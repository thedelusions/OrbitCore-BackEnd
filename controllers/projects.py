from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.project import ProjectModel
from models.vote import VoteModel
from serializers.project import ProjectSchema, ProjectResponseSchema, ProjectUpdateSchema
from database import get_db

router = APIRouter()

@router.post("/", response_model=ProjectResponseSchema)
def create_project(project: ProjectSchema, db: Session = Depends(get_db)):
    new_project = ProjectModel(
        title=project.title,
        description=project.description,
        ownerId=project.ownerId,
        status=project.status,
        tags=project.tags
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project

@router.get("/", response_model=List[ProjectResponseSchema])
def get_all_projects(db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponseSchema)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.put("/{project_id}", response_model=ProjectResponseSchema)
def update_project(project_id: int, project_update: ProjectUpdateSchema, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.status is not None:
        project.status = project_update.status
    if project_update.tags is not None:
        project.tags = project_update.tags
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.get("/user/{user_id}", response_model=List[ProjectResponseSchema])
def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).filter(ProjectModel.ownerId == user_id).all()
    return projects

@router.post("/{project_id}/upvote/{user_id}", response_model=ProjectResponseSchema)
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

@router.post("/{project_id}/downvote/{user_id}", response_model=ProjectResponseSchema)
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
