# Qanoon AI — Pakistani Law RAG Chatbot

## Overview

Qanoon AI is a Retrieval-Augmented Generation (RAG) chatbot developed to answer questions about the Islamabad Capital Territory Child Marriage Restraint Act, 2025.

The chatbot retrieves relevant information from the legal document and uses Google Gemini to generate context-based answers. It is designed to make legal information easier to understand through a simple, user-friendly chat interface.

## Features

- PDF text extraction and preprocessing
- Text chunking for document processing
- Text embeddings using Sentence Transformers
- Vector storage and similarity search using ChromaDB
- Retrieval-Augmented Generation (RAG) pipeline
- Context-based answer generation using Google Gemini
- LangGraph-based workflow
- Guardrails for handling user questions
- FastAPI backend
- Web-based chatbot interface
- API testing through Swagger UI

## Tech Stack

- **Programming Language:** Python
- **LLM:** Google Gemini
- **RAG Framework:** LangChain
- **Workflow Orchestration:** LangGraph
- **Embedding Model:** `all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB
- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```text
Pakistani_Law_Rag/
├── app/
│   ├── main.py
│   └── frontend/
│       └── index.html
├── src/
│   ├── preprocessing.py
│   ├── embedding.py
│   ├── retrieval.py
│   ├── guardrails.py
│   ├── prompts.py
│   ├── llm.py
│   ├── schemas.py
│   └── graph.py
├── data/
├── chroma_db/
├── test/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. **PDF Preprocessing:** Extracts text from the legal document.
2. **Text Chunking:** Divides the extracted text into smaller chunks.
3. **Embedding Generation:** Converts text chunks into numerical vectors using Sentence Transformers.
4. **Vector Storage:** Stores embeddings and their associated text in ChromaDB.
5. **Question Processing:** Receives a user's question through the chatbot interface.
6. **Information Retrieval:** Retrieves relevant document chunks using similarity search.
7. **Answer Generation:** Sends the question and retrieved context to Google Gemini.
8. **Response Delivery:** Returns the generated answer through the FastAPI backend to the chatbot interface.

## Installation and Setup

### Prerequisites

- Python installed on your system
- A Google Gemini API key
- An internet connection for API access and initial model downloads

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Pakistani_Law_Rag
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your actual API key. Never upload your real API key to GitHub.

### 5. Prepare the Vector Database

Ensure that the document preprocessing and embedding scripts have been executed and the ChromaDB collection has been created.

If the vector database already exists, verify that the application is configured to use the correct database path and collection.

## Running the Application

Start the FastAPI server from the project root:

```bash
python -m uvicorn app.main:app --reload
```

Once the server starts, open the following URLs:

- **Chatbot Interface:** http://127.0.0.1:8000/
- **Swagger API Documentation:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

Keep the terminal running while using the chatbot.

## API Usage

### Ask a Legal Question

**Endpoint:** `POST /ask`

Example request:

```json
{
  "question": "What is the main purpose of this Act?"
}
```

The API returns a response containing the answer and may include retrieved sources, scope information, and timing details, depending on the implementation.

## Future Improvements

- Improve response speed and error handling.
- Expand the legal document collection.
- Improve retrieval accuracy and answer evaluation.
- Add support for additional legal documents.

## Author

**Rehab Fatima**



