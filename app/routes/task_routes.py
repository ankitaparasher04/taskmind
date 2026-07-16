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
        if "PRIORITY:" in ai_result and "High" in ai_result:
            task.priority = "High"
        elif "PRIORITY:" in ai_result and "Low" in ai_result:
            task.priority = "Low"
        else:
            task.priority = "Medium"

        task.result = ai_result
        task.status = "completed"
        lines = ai_result.split("\n")

        inside_action_items = False

        for line in lines:

            clean_line = line.strip()

            if clean_line.startswith("ACTION ITEMS"):
                inside_action_items = True
                continue

            if clean_line.startswith("PRIORITY"):
                inside_action_items = False

            if inside_action_items and clean_line.startswith("-"):

                subtask_title = clean_line.replace("-", "").strip()

                subtask = Task(
                    title=subtask_title,
                    task_type="subtask",
                    status="pending",
                    priority=task.priority,
                    parent_id=task.id,
                    user_id=task.user_id
                )

                db.add(subtask)

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

    main_tasks = db.query(Task).filter(
        Task.user_id == user.id,
        Task.parent_id == None
    ).all()

    subtasks = db.query(Task).filter(
        Task.user_id == user.id,
        Task.parent_id != None
    ).all()

    main_task_data = []

    for main_task in main_tasks:
        related_subtasks = [
            subtask for subtask in subtasks
            if subtask.parent_id == main_task.id
        ]

        total = len(related_subtasks)

        completed = len([
            subtask for subtask in related_subtasks
            if subtask.status == "completed"
        ])

        progress = 0

        if total > 0:
            progress = int(
                (completed / total) * 100
            )

        main_task_data.append({
            "id": main_task.id,
            "title": main_task.title,
            "status": main_task.status,
            "priority": main_task.priority,
            "result": main_task.result,
            "total_subtasks": total,
            "completed_subtasks": completed,
            "progress": progress
        })

    return {
        "main_tasks": main_tasks,
        "subtasks": subtasks
    }

@router.put("/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == current_user
    ).first()

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        return {
            "error": "Task not found"
        }

    task.status = "completed"

    db.commit()

    return {
        "message": "Task completed"
    }