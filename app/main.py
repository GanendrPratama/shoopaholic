from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, AdminUpdateRequest
from .rag_engine import retrieve_context, rebuild_index
from .llm_client import call_kolosal_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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