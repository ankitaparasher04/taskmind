from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    task_type = Column(String)
    status = Column(String, default="pending")
    file_path = Column(String)

    result = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
