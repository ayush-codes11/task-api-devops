from fastapi import FastAPI

from app.db.database import engine
from app.models import Base


from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Task
from app.schemas import TaskCreate, TaskResponse


from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Task API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}







def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    db_task = Task(title=task.title)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task




@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()