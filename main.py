from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.users import router as UserRouter
from controllers.projects import router as ProjectRouter
from database import engine
from models.base import Base


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(UserRouter, prefix="/api")
app.include_router(ProjectRouter, prefix="/api")

@app.get('/')
def home():
    return {'message': 'Hello World!'}