from fastapi import FastAPI, Depends


from scr.app.auth.schemas import UserRead, UserCreate, UserUpdate
from scr.app.auth.manager import get_user_manager
from scr.app.auth.auth import auth_backend
from scr.app.auth.models import User

from scr.app.task_types.router import router as task_type_router
from scr.app.tasks.router import router as task_router 

from fastapi_users import FastAPIUsers


app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(task_router)
app.include_router(task_type_router)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/ping")
def pong():
    return {"ping": "pong!!!!"}

@app.get("/wow")
def wow_func():
    return {"result": "it's ok :)"}