🛍️ Shoopaholic

Shoopaholic is an intelligent, RAG-powered (Retrieval-Augmented Generation) shop assistant designed to bridge the gap between static shop data and dynamic customer queries.

It uses a **Hybrid AI Architecture**: simple, cost-effective local embeddings for searching through shop data, combined with a powerful Cloud LLM (via Kolosal AI) to generate natural, human-like answers.

**Live Demo**: [Shoopaholic Demo](https://shoopaholic-production.up.railway.app/)

---

## 🚀 Features

- **Hybrid RAG System**: Combines local HuggingFace models for privacy and speed during retrieval with a Cloud LLM for intelligent answer generation.
- **Secure Admin Dashboard**: Protected by a login system, allowing shop owners to manage inventory, update policies, and view analytics safely.
- **Single-Server Deployment**: FastAPI serves both the REST API and the static frontend files, eliminating the need for separate web servers.
- **Dual Interface**:
    - **Admin Dashboard**: For shop owners to manage inventory, update policies, and sync data to the AI.
    - **Customer Chat**: A clean, separate interface for customers to interact with the assistant.
- **Visual Responses**: The AI can intelligently surface product images directly in the chat.
- **Context-Aware**: The AI only answers based on the provided shop data, reducing hallucinations.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI (API + Static File Serving)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (No build tools required)
- **Retrieval Engine**: LlamaIndex + HuggingFace (BAAI/bge-small-en-v1.5) - Runs Locally
- **Generation Engine**: Kolosal AI (Llama 4 Maverick) - Accessed via direct REST API
- **Vector Store**: Local file persistence (LlamaIndex Storage)

---

## 📋 Prerequisites

- Python 3.9 or higher
- A Kolosal AI API Key

---

## ⚡ Quickstart Guide

### 1. Clone & Setup

```bash
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

### 2. Configure Environment

Create a `.env` file in the root directory and add your API key and admin credentials:

```env
KOLOSAI_API_KEY=your_actual_api_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Kolosal
```

> **Note**: If you do not set a username/password, it defaults to `admin` / `Kolosal`.

### 3. Run the Application

You only need one terminal to run the full stack.

```bash
# Run from the root folder
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the App

- **Admin Dashboard**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Customer Chat**: [http://localhost:8000/chat/](http://localhost:8000/chat/)

---

## 📂 Project Structure

```plaintext
shoopaholic/
├── .env                  # API Keys & Credentials (Do not commit this!)
├── requirements.txt      # Python dependencies
├── app/                  # Backend Application Source
│   ├── __init__.py
│   ├── config.py         # Config & Env loading
│   ├── schemas.py        # Pydantic Data Models
│   ├── rag_engine.py     # LlamaIndex Retrieval Logic
│   ├── llm_client.py     # Direct API Client (Kolosal wrapper)
│   └── main.py           # FastAPI Server & Static File Mounts
└── frontend/             # Frontend Source
        ├── admin/            # Admin Interface
        │   ├── index.html
        │   └── style.css
        └── chat/             # Customer Interface
                ├── index.html
                └── style.css
```

---

## 📖 How to Use

### Setup Shop (Admin)

1. Go to `/admin/`.
2. Login using the credentials set in your `.env` file.
3. Enter your Shop Name and Policies.
4. Add products with names, prices, and Image URLs.
5. **Crucial**: Click "✨ Sync Knowledge to AI". This builds the local vector index.

### Test Experience (Chat)

1. Go to `/chat/`.
2. Ask questions like:
     - "Do you have any red shoes?"
     - "What are your hours?"
3. If you added image URLs to your products, the bot will display them in the chat.

---

## 📦 Requirements

Ensure your `requirements.txt` contains:

```plaintext
fastapi
uvicorn
python-dotenv
requests
llama-index-core
llama-index-embeddings-huggingface
llama-index-readers-file
```