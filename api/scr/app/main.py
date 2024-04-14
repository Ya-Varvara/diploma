import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.scr.app.auth.router import router as auth_router
from api.scr.app.task_types.router import router as task_type_router
from api.scr.app.tasks.router import router as task_router
from api.scr.app.tests.router import router as test_router
from api.scr.app.forms.router import router as form_router
from api.scr.app.uploaded_files.router import router as upload_router

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)7s %(funcName)s:%(lineno)-5d %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    filename="my_logs.log",
)

origins = [
    "http://localhost:3000",  # Разрешить источник, где запущен ваш frontend
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
app.include_router(task_type_router)
app.include_router(test_router)
app.include_router(form_router)
app.include_router(upload_router)

logger.info("Start app")


@app.get("/ping")
def pong():
    return {"data": "pong!!!!"}
