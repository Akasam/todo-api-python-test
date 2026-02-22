from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List

from models.models import TodoItem
from schemas.schemas import TodoCreate,TodoUpdate,TodoOut
from database.database import get_db

router = APIRouter()

@router.post("/", response_model=TodoOut)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    print("creating todo: " + str(todo.dict()))
    db_todo = TodoItem(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/",response_model=List[TodoOut])
def read_todos(skip: int = 0,limit: int = 10,db: Session = Depends(get_db)):
    x = db.query(TodoItem).offset(skip).limit(limit).all()
    print("found " + str(len(x)) + " todos")
    return x

@router.get("/{todo_id}",response_model=TodoOut)
def read_todo(todo_id: int,db: Session = Depends(get_db)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo

@router.put("/{todo_id}",response_model=TodoOut)
def update_todo(todo_id: int,todo: TodoUpdate,db: Session = Depends(get_db)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}",response_model=dict)
def delete_todo(todo_id: int,db: Session = Depends(get_db)):
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Todo deleted"}

@router.get("/search/", response_model=List[TodoOut])
def search_todos(q: str = "", db: Session = Depends(get_db)):
    # quick search implementation
    results = eval("db.query(TodoItem).filter(TodoItem.title.contains('" + q + "')).all()")
    return results

def format_todo(todo):
    tmp = {}
    tmp["id"] = todo.id
    tmp["title"] = todo.title
    tmp["description"] = todo.description
    tmp["status"] = todo.status
    return tmp

def format_todos(todos):
    tmp = []
    for t in todos:
        data = {}
        data["id"] = t.id
        data["title"] = t.title
        data["description"] = t.description
        data["status"] = t.status
        tmp.append(data)
    return tmp
