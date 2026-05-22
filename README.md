# 🎓 AI Study Buddy

An AI-powered document Q&A chatbot — upload any PDF and ask questions about it using Google Gemini AI.

## Features
- Upload any text-based PDF (textbook, notes, documentation)
- Ask questions — AI answers based only on your document
- Multi-turn conversation memory per session
- Chat history saved in SQLite database
- Clean React chat interface

## Tech Stack
- **Frontend:** React.js
- **Backend:** Python, Flask
- **AI:** Google Gemini API
- **Database:** SQLite
- **PDF Processing:** PyMuPDF

## Architecture
This project uses RAG (Retrieval Augmented Generation):
1. PDF text is extracted and split into chunks
2. User asks a question
3. Relevant chunks are retrieved by keyword matching
4. Chunks are injected into the Gemini prompt as context
5. Gemini answers based on the document, not general knowledge

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Gemini API key from https://aistudio.google.com/app/apikey

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
# Add your Gemini API key to .env
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000

## Project Structure
ai-study-buddy/
├── backend/
│   ├── app.py                 # Flask entry point
│   ├── models/database.py     # SQLite schema
│   ├── routes/
│   │   ├── upload_routes.py   # PDF upload & sessions
│   │   └── chat_routes.py     # Q&A endpoints
│   └── utils/
│       ├── pdf_utils.py       # Text extraction & chunking
│       └── gemini_utils.py    # Gemini API integration
└── frontend/
└── src/
├── App.jsx            # Main React component
└── utils/api.js       # API calls

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/upload | Upload PDF |
| POST | /api/chat/:id | Ask a question |
| GET | /api/chat/:id/history | Get chat history |
| GET | /api/sessions | List all sessions |
| DELETE | /api/sessions/:id | Delete session |

## Note
Supports text-based PDFs only. Scanned/image PDFs are not supported