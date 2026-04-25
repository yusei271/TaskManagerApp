import logging
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    logger.info("Fetched all tasks")
    return tasks

@app.post("/tasks")
def add_task(title: str):
    db = SessionLocal()
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    logger.info(f"Task added: {title}")
    return task

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    logger.info(f"Task removed: {task_id}")
    return {"message": "removed"}
