# TaskMind

An AI-powered task management backend where users upload documents (e.g. resumes) 
and the system automatically analyzes them, classifies priority, and breaks the 
results into trackable subtasks — all processed asynchronously in the background.

## Features

- JWT-based authentication with per-user data isolation
- Document upload with automated AI-driven analysis
- Background processing (non-blocking) using multithreading
- AI-based priority classification (High / Medium / Low)
- Auto-generated subtasks from parsed AI output
- Task completion progress tracking

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · JWT · pypdf · Python threading

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Upload a document, create a task |
| GET | `/tasks` | Get user's tasks with subtasks & progress |
| PUT | `/tasks/{task_id}/complete` | Mark task as completed |

## Setup

\`\`\`bash
git clone https://github.com/ankitaparasher04/taskmind.git
cd taskmind
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# add DATABASE_URL, JWT_SECRET, AI_API_KEY to a local .env file
uvicorn app.main:app --reload
\`\`\`

## Roadmap

- Replace threading with Celery + Redis for reliable background jobs
- Add role-based access control (Admin/User)
- Docker containerization
