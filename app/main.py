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
from .database import mongo_db 

# Lifecycle Event to connect to DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure we connect to Mongo on startup
    try:
        mongo_db.connect()
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to MongoDB: {e}")
    yield

app = FastAPI(lifespan=lifespan)

# Global variable to store current shop text 
current_shop_context = "" 

# CORS Configuration - Allow All Origins for Development
# This effectively disables CORS restrictions for API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow ALL methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow ALL headers
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        log_query(request.query) 
        context_text = retrieve_context(request.query) 
        
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
         raise HTTPException(status_code=400, detail="Data cannot be empty")

    try:
        current_shop_context = request.shop_data_text
        rebuild_index(request.shop_data_text)
        return {"status": "success", "message": "Knowledge updated!"}
    except Exception as e:
        print(f"Update Knowledge Error: {e}")
        # Return 500 but log the specific error to console
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/admin/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        extracted_text = process_file(temp_path, file.filename)
        os.remove(temp_path)
        
        if not extracted_text:
            return {"status": "error", "text": "Could not extract text."}
            
        return {"status": "success", "text": extracted_text}
        
    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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