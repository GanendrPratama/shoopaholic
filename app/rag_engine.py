import os
import shutil
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .config import STORAGE_DIR

# Global Settings
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def load_knowledge_base():
    if not os.path.exists(STORAGE_DIR):
        return None
    try:
        # Check if the mandatory index files actually exist
        if not os.path.exists(os.path.join(STORAGE_DIR, "docstore.json")):
            return None
            
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        return load_index_from_storage(storage_context)
    except Exception as e:
        print(f"Error loading index: {e}")
        return None

def retrieve_context(query: str, top_k: int = 3) -> str:
    index = load_knowledge_base()
    if not index:
        return ""

    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    return "\n\n".join([node.get_content() for node in nodes])

def rebuild_index(text_data: str):
    # Ensure storage directory exists
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    # Note: We don't delete the whole dir anymore to avoid killing the analytics DB
    # LlamaIndex will overwrite the vector files automatically
    
    documents = [Document(text=text_data)]
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    return True