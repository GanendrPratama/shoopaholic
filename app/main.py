import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # New import for serving HTML
from .schemas import ChatRequest, AdminUpdateRequest
from .rag_engine import retrieve_context, rebuild_index
from .llm_client import call_kolosal_api

app = FastAPI()

# CORS is still good to keep, though less critical if serving from same origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints (Must be defined BEFORE static files) ---

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Retrieve relevant info from local DB
        context_text = retrieve_context(request.query)
        
        if not context_text:
            return {"answer": "I don't have any shop information yet. Please ask the admin to upload data."}

        # 2. Send context + question to Cloud LLM
        answer = call_kolosal_api(context_text, request.query)
        
        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"answer": f"System Error: {str(e)}"}

@app.post("/admin/update_knowledge")
async def update_knowledge(request: AdminUpdateRequest):
    if not request.shop_data_text.strip():
         raise HTTPException(status_code=400, detail="Data cannot be empty")

    try:
        rebuild_index(request.shop_data_text)
        return {"status": "success", "message": "Knowledge base updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Static File Serving ---
# We calculate the path to the 'frontend' folder relative to this file
# This allows us to serve the HTML/CSS/JS directly
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(os.path.dirname(current_dir), "frontend")

# Mount the frontend directory to the root "/"
# html=True allows visiting /admin/ to automatically find /admin/index.html
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
else:
    print("⚠️ Warning: Frontend directory not found. Creating server without UI.")