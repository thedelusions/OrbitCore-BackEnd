from fastapi import FastAPI
from controllers.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, prefix="/api")

@app.get('/')
def home():
    return 'Hello World!'