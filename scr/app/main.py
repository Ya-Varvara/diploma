from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!!!!"}

@app.get("/wow")
def wow_func():
    return {"result": "it's ok :)"}