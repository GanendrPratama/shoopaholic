import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import ADMIN_USERNAME, ADMIN_PASSWORD
from .schemas import ChatRequest, AdminUpdateRequest, LoginRequest
from .rag_engine import retrieve_context, rebuild_index
from .llm_client import call_kolosal_api
from .analytics import init_db, log_query, get_analytics_data, generate_recommendations

app = FastAPI()

# Initialize DB on startup
init_db()

# Global variable to store current shop text for recommendation logic
# In a real app, this would be in a database, but memory is fine for this scale.
current_shop_context = "" 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LOGIN ENDPOINT ---
@app.post("/admin/login")
async def admin_login(creds: LoginRequest):
    # Verify against environment variables
    if creds.username == ADMIN_USERNAME and creds.password == ADMIN_PASSWORD:
        return {"status": "success", "message": "Logged in"}
    
    # Return 401 Unauthorized if failed
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Log the query for analytics
        log_query(request.query)

        # 2. Retrieve context
        context_text = retrieve_context(request.query)
        if not context_text:
            return {"answer": "I don't have that information. Please contact the owner."}

        # 3. Generate Answer
        answer = call_kolosal_api(context_text, request.query)
        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"answer": "Sorry, I'm having trouble connecting to the brain."}

@app.post("/admin/update_knowledge")
async def update_knowledge(request: AdminUpdateRequest):
    global current_shop_context
    if not request.shop_data_text.strip():
         raise HTTPException(status_code=400, detail="Data cannot be empty")

    try:
        # Save text to memory for recommendation engine to check against
        current_shop_context = request.shop_data_text
        
        rebuild_index(request.shop_data_text)
        return {"status": "success", "message": "Knowledge updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW ANALYTICS ENDPOINTS ---

@app.get("/admin/analytics")
async def get_stats():
    return get_analytics_data()

@app.get("/admin/recommendations")
async def get_suggestions():
    return {"msgs": generate_recommendations(current_shop_context)}

# --- Static Files ---
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")