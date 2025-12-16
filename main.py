from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.users import router as UserRouter
from controllers.projects import router as ProjectRouter
from database import engine
from models.base import Base
from models.user import UserModel
from models.project import ProjectModel
from models.vote import VoteModel
from models.team import TeamModel


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter, prefix="/api")
app.include_router(ProjectRouter, prefix="/api")

@app.get('/')
def home():
    return {'message': 'Hello World!'}