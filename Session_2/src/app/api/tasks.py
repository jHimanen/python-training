from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(User, payload.user_id):
        raise HTTPException(404, "User does not exist")
    task = Task(user_id=payload.user_id, title=payload.title, completed=False)
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.get("", response_model=list[TaskOut])
def list_tasks(
    user_id: int | None = None,
    completed: bool | None = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Task)
    if user_id is not None:
        q = q.filter(Task.user_id == user_id)
    if completed is not None:
        q = q.filter(Task.completed == completed)
    return q.order_by(Task.id.desc()).all()

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    if payload.title is not None:
        task.title = payload.title
    if payload.completed is not None:
        task.completed = payload.completed
    db.commit(); db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        return
    db.delete(task); db.commit()
