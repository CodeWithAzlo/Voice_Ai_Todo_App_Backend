from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
import json
from sqlalchemy import func

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- CREATE TODO ----------------
@router.post("/create_todo/")
def create_todos(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = next(
        (c for c in request.message.toolCalls if c.function.name == "createTodo"), None
    )
    if not tool_call:
        raise HTTPException(status_code=400, detail="Invalid Request")

    args = tool_call.function.arguments
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in arguments")

    todo = models.Todo(title=args.get("title", ""), description=args.get("description", ""))
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return {"results": [{"todoCallId": tool_call.id, "result": "success"}]}


# ---------------- GET TODOS ----------------
@router.post("/get_todos/")
def get_todos(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = next(
        (c for c in request.message.toolCalls if c.function.name == "getTodos"), None
    )
    if not tool_call:
        raise HTTPException(status_code=400, detail="Invalid Request")

    todos = db.query(models.Todo).all()

    return {
        "results": [
            {
                "todoCallId": tool_call.id,
                "result": [schemas.TodoResponse.from_orm(todo).dict() for todo in todos],
            }
        ]
    }


# ---------------- COMPLETE TODO ----------------
@router.post("/complete_todo/")
def complete_todo(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = next(
        (c for c in request.message.toolCalls if c.function.name == "completeTodo"), None
    )
    if not tool_call:
        raise HTTPException(status_code=400, detail="Invalid Request")

    args = tool_call.function.arguments
    if isinstance(args, str):
        args = json.loads(args)

    todo_id = args.get("id")
    if not todo_id:
        raise HTTPException(status_code=400, detail="Missing To-Do ID")

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = True
    db.commit()
    db.refresh(todo)

    return {"results": [{"todoCallId": tool_call.id, "result": "success"}]}


# ---------------- DELETE TODO ----------------
@router.post("/delete_todo/")
def delete_todo(request: schemas.VapiRequest, db: Session = Depends(get_db)):
    tool_call = next(
        (c for c in request.message.toolCalls if c.function.name == "deleteTodo"), None
    )
    if not tool_call:
        raise HTTPException(status_code=400, detail="Invalid Request")

    args = tool_call.function.arguments
    if isinstance(args, str):
        args = json.loads(args)

    todo_id = args.get("id")
    title = args.get("title")

    todo = None

    if todo_id is not None:
        if not isinstance(todo_id, int):
            raise HTTPException(status_code=400, detail="Invalid To-Do ID: must be an integer")
        todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    elif title:
        todo = db.query(models.Todo).filter(func.lower(models.Todo.title) == title.lower()).first()
    else:
        raise HTTPException(status_code=400, detail="Provide either 'id' or 'title' to delete")

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with title '{title}' not found")

    db.delete(todo)
    db.commit()

    return {"results": [{"todoCallId": tool_call.id, "result": "success"}]}
