from fastapi import FastAPI
from controllers.users import router as UserRouter
from controllers.projects import router as ProjectRouter

app = FastAPI()

app.include_router(UserRouter, prefix="/api")
app.include_router(ProjectRouter, prefix="/api")

@app.get('/')
def home():
    return 'Hello World!'