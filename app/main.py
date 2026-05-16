from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.task import Task
from app.routes.user_routes import router as user_router
from fastapi import Depends
from app.auth.oauth2 import get_current_user

from dotenv import load_dotenv

load_dotenv()


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)


templates = Jinja2Templates(directory="app/templates")

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)




@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
    )

@app.get("/signup-page", response_class=HTMLResponse)
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html"
    )
@app.get(
    "/login-page",
    response_class=HTMLResponse
)

def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)

def dashboard(

    request: Request
):
    # current_user = get_current_user(token)

    db = SessionLocal()

    # user = db.query(User).filter(
    #     User.email == current_user
    # ).first()

    # tasks = db.query(Task).filter(
    #     Task.user_id == user.id
    # ).all()


    tasks = db.query(Task).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            # "current_user": current_user,
            "tasks": tasks
        }
    )


from app.routes.task_routes import (
    router as task_router
)
app.include_router(task_router)