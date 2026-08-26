# FastAPI Health API

A minimal FastAPI application with a health-check endpoint.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
Windows PowerShell
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Run the application
uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

Health Check

Send a GET request to:

GET /health

Expected response:

{
  "status": "ok"
}
API Documentation

FastAPI automatically provides interactive documentation:

/docs — Swagger UI
/redoc — ReDoc