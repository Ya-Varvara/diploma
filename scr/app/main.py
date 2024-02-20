from fastapi import FastAPI, Depends


from scr.app.auth.router import router as auth_router, get_current_user
from scr.app.core.models import User
from scr.app.task_types.router import router as task_type_router
from scr.app.tasks.router import router as task_router
from scr.app.tests.router import router as test_router
from scr.app.test_tasks.router import router as test_task_router
from scr.app.test_task_results.router import router as test_task_result_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(task_type_router)
app.include_router(test_router)
app.include_router(test_task_router)
app.include_router(test_task_result_router)


@app.get("/protected-route")
def protected_route(user: User = Depends(get_current_user())):
    return f"Hello, {user.email}"


@app.get("/ping")
def pong():
    return {"ping": "pong!!!!"}
