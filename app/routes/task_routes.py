from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task_schema import TaskCreate

from app.models.user import User
from app.auth.oauth2 import get_current_user

from app.database import SessionLocal
import threading
import time
from fastapi import UploadFile, File, Form

from pypdf import PdfReader

from app.services.ai_service import (
    analyze_resume
)

def process_task(task_id):

    print("THREAD STARTED")

    db = SessionLocal()

    try:
        task = db.query(Task).filter(
            Task.id == task_id
        ).first()

        print("TASK FOUND")

        task.status = "processing"
        db.commit()

        print("TASK PROCESSING")

        time.sleep(5)

        reader = PdfReader(task.file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        ai_result = analyze_resume(text)

        task.result = ai_result
        task.status = "completed"

        db.commit()
        

        print("TASK COMPLETED")

    except Exception as e:

        task.status = "failed"
        task.result = f"AI processing failed: {str(e)}"

        db.commit()

        print("TASK FAILED", e)

    finally:

        db.close()

router = APIRouter()

@router.post("/tasks")
def create_task(
    file: UploadFile = File(...),
    task_type: str = Form(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == current_user
    ).first()

    file_location = (
        f"app/uploads/{file.filename}"
    )

    with open(
        file_location,
        "wb"
    ) as buffer:

        buffer.write(
            file.file.read()
        )

    new_task = Task(
        title=file.filename,
        task_type=task_type,
        status="pending",
        file_path=file_location,
        user_id=user.id
    )

    db.add(new_task)

    db.commit()
    db.refresh(new_task)

    thread = threading.Thread(
        target=process_task,
        args=(new_task.id, )
    )

    thread.start()

    return {
        "message": "Task created successfully"
    }

@router.get("/tasks")
def get_tasks(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == current_user
    ).first()

    tasks = db.query(Task).filter(
        Task.user_id == user.id
    ).all()

    return tasks