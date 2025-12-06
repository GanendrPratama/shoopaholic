import os
import shutil
from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .config import PERSIST_DIR

# Initialize Settings once (Global configuration)
# We set LLM to None because we use llm_client.py for generation
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def load_knowledge_base():
    """Loads the existing vector index from disk."""
    if not os.path.exists(PERSIST_DIR):
        return None
    try:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)
    except Exception as e:
        print(f"Error loading index: {e}")
        return None

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Searches the database and returns the text chunks as a single string."""
    index = load_knowledge_base()
    if not index:
        return ""

    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)
    
    # Combine all found text chunks into one block
    return "\n\n".join([node.get_content() for node in nodes])

def rebuild_index(text_data: str):
    """Wipes old data and creates a new index from the provided text."""
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)

    documents = [Document(text=text_data)]
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return True