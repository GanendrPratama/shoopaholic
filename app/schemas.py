from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

class AdminUpdateRequest(BaseModel):
    shop_data_text: str