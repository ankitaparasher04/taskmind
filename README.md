# TaskMind

TaskMind is an AI-powered task management backend built with FastAPI that allows users to upload documents (such as resumes), automatically analyze them using AI, classify priorities, and generate trackable subtasks.

The system processes heavy operations asynchronously in the background, ensuring a fast and responsive user experience.

---

## Features

* JWT-based authentication and authorization
* Per-user data isolation
* Document upload and processing
* AI-powered document analysis
* Automatic priority classification (High / Medium / Low)
* Automatic subtask generation
* Background processing using multithreading
* Task completion tracking
* Progress monitoring
* RESTful API architecture

---

## Tech Stack

### Backend

* FastAPI
* Python
* SQLAlchemy
* PostgreSQL

### Authentication

* JWT Authentication

### AI & Document Processing

* AI API Integration
* pypdf

### Background Processing

* Python Threading

---

## Project Structure

```text
taskmind/

├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database/
│   └── main.py
│
├── uploads/
├── requirements.txt
├── .env
└── README.md
```

---

## Workflow

1. User registers and logs in.
2. User uploads a document.
3. A new task is created.
4. The document is processed in the background.
5. AI analyzes the content.
6. Priority is assigned automatically.
7. Subtasks are generated.
8. Users can track progress and mark tasks as completed.

---

## API Endpoints

| Method | Endpoint                    | Description                              |
| ------ | --------------------------- | ---------------------------------------- |
| POST   | `/auth/register`            | Register a new user                      |
| POST   | `/auth/login`               | Login and receive JWT token              |
| POST   | `/tasks`                    | Upload a document and create a task      |
| GET    | `/tasks`                    | Get all tasks with subtasks and progress |
| PUT    | `/tasks/{task_id}/complete` | Mark a task as completed                 |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ankitaparasher04/taskmind.git

cd taskmind
```

---

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create a `.env` file

Create a `.env` file in the root directory and add:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/taskmind

JWT_SECRET=your_secret_key

AI_API_KEY=your_ai_api_key
```

---

### 5. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE taskmind;
```

Update the `DATABASE_URL` in your `.env` file accordingly.

---

### 6. Run database migrations

If you are using Alembic:

```bash
alembic upgrade head
```

---

### 7. Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Example Use Case

A user uploads a resume.

TaskMind:

* Extracts information from the document.
* Sends it for AI analysis.
* Assigns a priority level.
* Generates actionable subtasks.
* Tracks completion progress.

---

## Future Roadmap

### Backend Improvements

* Replace multithreading with Celery + Redis.
* Add role-based access control (Admin/User).
* Add email notifications.
* Add logging and monitoring.

### DevOps

* Docker containerization.
* Docker Compose setup.
* CI/CD pipeline.
* Production deployment.

### AI Features

* Resume scoring.
* ATS compatibility checks.
* Smart recommendations.
* AI-generated summaries.

---

## Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push to GitHub.

```bash
git push origin feature-name
```

5. Open a Pull Request.


---

## Author

**Ankita Parasher**

* GitHub: https://github.com/ankitaparasher04

