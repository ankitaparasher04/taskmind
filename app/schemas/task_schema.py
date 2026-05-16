from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    task_type: str