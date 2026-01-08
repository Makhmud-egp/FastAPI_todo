from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# from fastapi.templating import Jinja2Templates
# ============================================
# QADAM 3.1: App yaratish (DOIM SHUNDAY!)
# ============================================
app = FastAPI()
# ============================================
# QADAM 3.2: Jadvallarni yaratish (DOIM SHUNDAY!)
# ============================================
models.Base.metadata.create_all(bind=engine)
# BU QATOR JUDA MUHIM!
# Loyihani birinchi ishga tushirganda todos.db fayli yaratiladi
# ------------------- Templates ----------------------

# templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory='static'), name='static')



@app.get('/')
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)





# ------------------ Include AUTH Router --------

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)