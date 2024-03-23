from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.scr.app.auth.router import router as auth_router
from api.scr.app.task_types.router import router as task_type_router
from api.scr.app.tasks.router import router as task_router
from api.scr.app.tests.router import router as test_router
from api.scr.app.test_tasks.router import router as test_task_router
from api.scr.app.test_task_results.router import router as test_task_result_router


origins = [
    "http://localhost:3000",  # Разрешить источник, где запущен ваш frontend
    "http://localhost:8000",  # Опционально, если вы также делаете запросы на сам backend
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(auth_router)
# app.include_router(task_router)
app.include_router(task_type_router)
# app.include_router(test_router)
# app.include_router(test_task_router)
# app.include_router(test_task_result_router)


@app.get("/ping")
def pong():
    return {"data": "pong!!!!"}
