from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.project import ProjectModel
from models.user import UserModel
from models.vote import VoteModel
from models.request import RequestModel
from serializers.project import ProjectSchema, ProjectResponseSchema, ProjectUpdateSchema
from database import get_db
from dependencies.get_current_user import get_current_user
router = APIRouter()

@router.post("/projects/", response_model=ProjectResponseSchema)
def create_project(project: ProjectSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    new_project = ProjectModel(
        title=project.title,
        description=project.description,
        ownerId=current_user.id,
        status=project.status,
        tags=project.tags,
        repo_link=project.repo_link
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project

@router.get("/projects/", response_model=List[ProjectResponseSchema])
def get_all_projects(db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).all()
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponseSchema)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponseSchema)
def update_project(project_id: int, project_update: ProjectUpdateSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.ownerId != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this project")
    
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.status is not None:
        project.status = project_update.status
    if project_update.tags is not None:
        project.tags = project_update.tags
    if project_update.repo_link is not None:
        project.repo_link = project_update.repo_link
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.ownerId != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    
    db.query(VoteModel).filter(VoteModel.projectId == project_id).delete()
    db.query(RequestModel).filter(RequestModel.project_id == project_id).delete()
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.get("/projects/user/{user_id}", response_model=List[ProjectResponseSchema])
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).filter(ProjectModel.ownerId == user_id).all()
    return projects

@router.post("/projects/{project_id}/upvote/{user_id}", response_model=ProjectResponseSchema)
def upvote_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing_vote = db.query(VoteModel).filter(
        VoteModel.userId == user_id,
        VoteModel.projectId == project_id
    ).first()
    
    if existing_vote:
        if existing_vote.voteType == "upvote":
            raise HTTPException(status_code=400, detail="You already upvoted this project")
        else:
            project.downvotes -= 1
            project.upvotes += 1
            existing_vote.voteType = "upvote"
    else:
        project.upvotes += 1
        new_vote = VoteModel(userId=user_id, projectId=project_id, voteType="upvote")
        db.add(new_vote)
    
    db.commit()
    db.refresh(project)
    
    return project

@router.post("/projects/{project_id}/downvote/{user_id}", response_model=ProjectResponseSchema)
def downvote_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing_vote = db.query(VoteModel).filter(
        VoteModel.userId == user_id,
        VoteModel.projectId == project_id
    ).first()
    
    if existing_vote:
        if existing_vote.voteType == "downvote":
            raise HTTPException(status_code=400, detail="You already downvoted this project")
        else:
            project.upvotes -= 1
            project.downvotes += 1
            existing_vote.voteType = "downvote"
    else:
        project.downvotes += 1
        new_vote = VoteModel(userId=user_id, projectId=project_id, voteType="downvote")
        db.add(new_vote)
    
    db.commit()
    db.refresh(project)
    
    return project
