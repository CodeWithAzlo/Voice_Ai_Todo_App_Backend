# 🎤 Voice Todo AI

A **voice-controlled To-Do application** powered by **FastAPI**, **VAPI**, **Twilio**, and **PostgreSQL**.  
Manage your tasks using **voice commands** with AI assistance.

---

## 🚀 Features

- **Create, view, complete, and delete todos** using voice commands.
- Integration with **VAPI** for AI assistant interaction.
- **Twilio voice integration** to manage your todos via phone.
- **NGROK support** for exposing your local FastAPI server to the public.
- Fully **modular and scalable code structure** with SQLAlchemy ORM.
- Environment variables support for secure configuration.

---

## 📁 Folder Structure
```
voice_todo_ai/
│
├─ app/
│ ├─ init.py
│ ├─ main.py # FastAPI app
│ ├─ models.py # SQLAlchemy models
│ ├─ schemas.py # Pydantic schemas
│ ├─ database.py # DB connection and SessionLocal
│ └─ routes/
│ ├─ init.py
│ └─ todo.py # All todo-related endpoints
│
├─ .env.example # Sample environment variables
├─ requirements.txt
└─ README.md
```

---

## ⚡ Requirements

- Python >= 3.10
- PostgreSQL
- Twilio account for voice calls
- VAPI account for AI integration
- NGROK for public URL access

---

## 🛠 Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd voice_todo_ai

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Create a .env file (or copy .env.example) and fill your credentials:

DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<dbname>
VAPI_API_KEY=<your-vapi-api-key>
TWILIO_ACCOUNT_SID=<your-twilio-sid>
TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
TWILIO_PHONE_NUMBER=<your-twilio-number>

Run FastAPI server:

uvicorn app.main:app --reload

Expose local server with NGROK:

ngrok http 8000

📝 API Usage
Create Todo

POST /create_todo/

{
  "message": {
    "toolCalls": [
      {
        "id": "1",
        "function": {
          "name": "createTodo",
          "arguments": {
            "title": "Buy milk",
            "description": "From the store"
          }
        }
      }
    ]
  }
}

Response:
{
  "results": [
    {
      "todoCallId": "1",
      "result": "success"
    }
  ]
}

Get Todos

POST /get_todos/
{
  "message": {
    "toolCalls": [
      {
        "id": "2",
        "function": {
          "name": "getTodos",
          "arguments": {}
        }
      }
    ]
  }
}

Response:
{
  "results": [
    {
      "todoCallId": "2",
      "result": [
        {
          "id": 1,
          "title": "Buy milk",
          "description": "From the store",
          "completed": false
        }
      ]
    }
  ]
}

Complete Todo

POST /complete_todo/
{
  "message": {
    "toolCalls": [
      {
        "id": "3",
        "function": {
          "name": "completeTodo",
          "arguments": {
            "id": 1
          }
        }
      }
    ]
  }
}

Delete Todo

POST /delete_todo/
{
  "message": {
    "toolCalls": [
      {
        "id": "4",
        "function": {
          "name": "deleteTodo",
          "arguments": {
            "id": 1
          }
        }
      }
    ]
  }
}

💡 How it works

Voice commands are sent to your voice AI assistant.

The AI calls FastAPI endpoints via toolCalls.

FastAPI interacts with PostgreSQL to create, update, or delete todos.

Twilio integration allows voice control over phone calls.

NGROK exposes your local server for testing with VAPI and Twilio.

🧑‍💻 Author

CodeWithAzlo 💖
Email: codewithazlo@gmail.com


