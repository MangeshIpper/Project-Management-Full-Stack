from fastapi import APIRouter, Depends, HTTPException
from schamas.task import TaskCreate
from database import session, get_db
from models.task import Task
from security.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/get-tasks")
def get_tasks(db = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
        return tasks
    except Exception as e:
        print(f"Error {e}")
        
        
        
@router.get("/get-task/{id}")
def get_task_by_id(id:int, db = Depends(get_db), current_user = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id).first()
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/create-task")
def create_task(task: TaskCreate, db = Depends(get_db), current_user = Depends(get_current_user)):
    new_task = Task(**task.model_dump(), user_id = current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/update-task")
def update_task(id:int,task:TaskCreate,db = Depends(get_db),current_user = Depends(get_current_user)):
    task_exist = db.query(Task).filter(Task.id == id).first()
    if task_exist.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Not authorized to access this task")
    if not task_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    for key , value in task.model_dump().items():
        setattr(task_exist,key,value)
    db.commit()
    db.refresh(task_exist)
        
    # OR
    
    # task_exist.title = task.title
    # task_exist.description = task.description
    # task_exist.completed = task.completed
    # db.commit()
    # db.refresh(task_exist)

    return task_exist


@router.delete("/delete-task")
def delete_task(id:int, db=Depends(get_db), current_user = Depends(get_current_user)):
    task_exist = db.query(Task).filter(Task.id == id).first()
    if task_exist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    if not task_exist:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_exist)
    db.commit()
    return {"message":"Task is deleted successfully"}