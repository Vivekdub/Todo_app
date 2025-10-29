from fastapi import FastAPI, Depends, HTTPException, status
from .db import Base, engine, SessionLocal
from . import models, auth, scheduler
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Schemas
class SignupIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

# Simple signup/login
@app.post("/api/auth/signup")
def signup(data: SignupIn):
    db = SessionLocal()
    try:
        user = models.User(email=data.email, password_hash=auth.hash_password(data.password))
        db.add(user)
        db.commit()
        return {"msg":"created"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        db.close()

@app.post("/api/auth/login")
def login(data: LoginIn):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == data.email).first()
        if not user or not auth.verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = auth.create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload: raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.close()
    if not user: raise HTTPException(status_code=401, detail="User not found")
    return user

# Tasks endpoints (simple)
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    due_at: Optional[datetime] = None

class TaskOut(TaskIn):
    id: int
    is_completed: bool
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime | None

@app.get("/api/tasks", response_model=List[TaskOut])
def list_tasks(current_user=Depends(get_current_user)):
    db = SessionLocal()
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    db.close()
    return tasks

@app.post("/api/tasks")
def create_task(payload: TaskIn, current_user=Depends(get_current_user)):
    db = SessionLocal()
    task = models.Task(user_id=current_user.id, title=payload.title, description=payload.description, due_at=payload.due_at)
    db.add(task); db.commit(); db.refresh(task)
    db.close()
    return task

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, payload: TaskIn, current_user=Depends(get_current_user)):
    db = SessionLocal()
    task = db.query(models.Task).filter(models.Task.id==task_id, models.Task.user_id==current_user.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    task.title = payload.title
    task.description = payload.description
    task.due_at = payload.due_at
    task.reminder_sent = False  # reset if due date changed
    db.add(task); db.commit(); db.refresh(task); db.close()
    return task

@app.post("/api/tasks/{task_id}/complete")
def complete_task(task_id: int, current_user=Depends(get_current_user)):
    db = SessionLocal()
    task = db.query(models.Task).filter(models.Task.id==task_id, models.Task.user_id==current_user.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    task.is_completed = True
    db.add(task); db.commit(); db.close()
    return {"msg":"ok"}

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user)):
    db = SessionLocal()
    task = db.query(models.Task).filter(models.Task.id==task_id, models.Task.user_id==current_user.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task); db.commit(); db.close()
    return {"msg":"deleted"}

# Start scheduler on startup
@app.on_event("startup")
def on_startup():
    scheduler.start_scheduler()
