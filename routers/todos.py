from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos, TodoRequest
from database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# BU FUNKSIYANI YODLAB OLING!
# Har bir loyihada BIR XILDA!

# ============================================
# QADAM 3.4: Dependency Annotation (DOIM SHUNDAY!)
# ============================================

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

# ============================================
# QADAM 3.5: CRUD Operatsiyalar
# ============================================


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response



### Pages ###
@router.get('/todo-page')
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

        return templates.TemplateResponse("todos.html", {'request': request, "todos": todos, "user": user})

    except:
        return redirect_to_login()



@router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

    except:
        return redirect_to_login()



@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, db: db_dependency, todo_id: int):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    except:
        return redirect_to_login()




# ------------- Read All Todos (GET) -----------
@router.get("/", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()



# ------------- Read Single (Todo) (GET) -----------
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .filter(Todos.owner_id == user.get('id')).first()

    if todo_model is not None:
        return todo_model



    raise HTTPException(status_code=404, detail="Todo not found")


# ------------- Create (POST) -----------------
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      todo_request: TodoRequest,
                      db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")


    new_todo = Todos(
        **todo_request.model_dump(),
        owner_id=user.get('id'))

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# ------------- Update (PUT) --------------------
@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                      todo_request: TodoRequest,
                      db: db_dependency,
                      todo_id: int = Path(gt=0)):
    # Agar user login qimagan bosa JWT tokeni bomasa
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")


    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()


    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# ------------- Delete (DELETE) --------------------
@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                                .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id)\
                    .filter(Todos.owner_id == user.get('id')).delete()


    db.commit()
