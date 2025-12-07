import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from .schemas import ChatRequest, AdminUpdateRequest
from .rag_engine import retrieve_context, rebuild_index
from .llm_client import call_kolosal_api
from .analytics import log_query, get_analytics_data, generate_recommendations
from .file_processor import process_file
from .database import mongo_db # Import the DB instance

# Lifecycle Event to connect to DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_db.connect()
    yield

app = FastAPI(lifespan=lifespan)

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

current_shop_context = "" 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        log_query(request.query) # Now writes to Mongo
        context_text = retrieve_context(request.query) # Now reads from Elastic
        
        if not context_text:
            context_text = "No shop data found."
            
        answer = call_kolosal_api(context_text, request.query)
        return {"answer": answer}
    except Exception as e:
        print(f"Error: {e}")
        return {"answer": f"System Error: {str(e)}"}

@app.post("/admin/update_knowledge")
async def update_knowledge(request: AdminUpdateRequest):
    global current_shop_context
    if not request.shop_data_text.strip():
         raise HTTPException(status_code=400, detail="Empty data")
    try:
        current_shop_context = request.shop_data_text
        rebuild_index(request.shop_data_text) # Writes to Elastic
        return {"status": "success", "message": "Knowledge updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")