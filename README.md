🛍️ Shoopaholic

Shoopaholic is an intelligent, RAG-powered (Retrieval-Augmented Generation) shop assistant designed to bridge the gap between static shop data and dynamic customer queries.

It uses a Hybrid AI Architecture: simple, cost-effective local embeddings for searching through shop data, combined with a powerful Cloud LLM (via Kolosal AI) to generate natural, human-like answers.

🚀 Features

- Hybrid RAG System: Uses local HuggingFace models for privacy and speed during retrieval, and a Cloud LLM for intelligent answer generation.

- Admin Dashboard: Simple interface for shop owners to paste product catalogs, promotions, and policy updates instantly.

- Context-Aware: The AI only answers based on the provided shop data, reducing hallucinations.

- Modular Codebase: Organized architecture separating the API client, RAG engine, and server logic.

- Cost-Effective: Retrieval happens locally (free), minimizing API costs to only the final answer generation.

🛠️ Tech Stack

- Backend: Python, FastAPI

- Frontend: HTML5, CSS3, Vanilla JavaScript

- AI Framework: LlamaIndex (for Vector Store & Retrieval)

- Embeddings: HuggingFace (BAAI/bge-small-en-v1.5) - Runs Locally

- LLM Service: Kolosal AI (Llama 4 Maverick) - Accessed via standard REST API

- Vector Store: Local file persistence (LlamaIndex Storage)

📋 Prerequisites

- Python 3.9 or higher

- A Kolosal AI API Key

⚡ Quickstart Guide

1. Clone & Setup

```
# Clone the repository
git clone https://github.com/yourusername/shoopaholic.git
cd shoopaholic


# Create a virtual environment (Recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```


2. Configure Environment

Create a .env file in the root directory (next to requirements.txt) and add your API key:
```
KOLOSAI_API_KEY=your_actual_api_key_here
```

3. Run the Application

You need two terminal windows open to run the full stack.

Terminal 1: Start the Backend (The Brain)
```bash
# Run from the root folder
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2: Start the Frontend (The UI)
```bash
cd frontend
python -m http.server 5500
```

4. Access the App

Open your browser and navigate to:
👉 http://localhost:5500

📂 Project Structure
```
shoopaholic/
├── .env                  # API Keys (Do not commit this!)
├── requirements.txt      # Python dependencies
├── app/                  # Backend Application Source
│   ├── __init__.py       # Package marker
│   ├── config.py         # Config & Env loading
│   ├── schemas.py        # Pydantic Data Models
│   ├── rag_engine.py     # LlamaIndex Retrieval Logic
│   ├── llm_client.py     # Direct API Client (Curl wrapper)
│   └── main.py           # FastAPI Server Endpoints
└── frontend/             # Frontend Source
    └── index.html        # Single-page UI
```

📖 How to Use

For Shop Owners (Admin Panel - Left Side):

Paste your product list, prices, and current promotions into the text area.

Click "Update Knowledge Base".

Wait for the success message. The AI has now indexed your data locally into a vector store.

For Customers (Chat Panel - Right Side):

Ask questions like "Do you have any running shoes?" or "What is your return policy?".

The bot will search your local index, find relevant context, and send it to Llama 4 Maverick to generate a helpful response.

📦 Recommended Requirements

Ensure your requirements.txt contains the following:
```
fastapi
uvicorn
python-dotenv
requests
llama-index-core
llama-index-embeddings-huggingface
llama-index-readers-file
```