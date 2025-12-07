import os
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.elasticsearch import ElasticsearchStore

# Config
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")
INDEX_NAME = "shoopaholic_vectors"

# Global Settings (Embedding Model)
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def get_vector_store():
    """Connects to Elasticsearch"""
    return ElasticsearchStore(
        es_url=ELASTIC_URL,
        index_name=INDEX_NAME,
    )

def retrieve_context(query: str, top_k: int = 3) -> str:
    try:
        vector_store = get_vector_store()
        
        # Load index from existing vector store
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        retriever = index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        
        return "\n\n".join([node.get_content() for node in nodes])
    except Exception as e:
        print(f"⚠️ Retrieval Error (Is Elastic running?): {e}")
        return ""

def rebuild_index(text_data: str):
    try:
        vector_store = get_vector_store()
        
        # Create documents
        documents = [Document(text=text_data)]
        
        # Create storage context pointing to Elastic
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # This automatically embeds the text and sends it to Elasticsearch
        VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context
        )
        print("✅ Data indexed in Elasticsearch")
        return True
    except Exception as e:
        print(f"❌ Indexing Error: {e}")
        raise e