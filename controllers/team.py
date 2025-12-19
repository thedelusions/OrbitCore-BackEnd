from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from models.team import TeamModel
from models.user import UserModel
from models.project import ProjectModel
from models.comment import CommentModel
from serializers.team import TeamSchema, TeamResponseSchema
from serializers.comment import CommentSchema, CommentResponseSchema
from database import get_db
from dependencies.get_current_user import get_current_user
import jwt
from config.environment import secret


router = APIRouter()

def is_team_member(project_id: int, user_id: int, db: Session):
    return db.query(TeamModel).filter(
        TeamModel.project_id == project_id,
        TeamModel.user_id == user_id
    ).first() is not None


@router.get("/projects/{project_id}/team", response_model=list[TeamResponseSchema])
def get_team_members(project_id: int, db: Session = Depends(get_db)):
    team_members = db.query(TeamModel).filter(TeamModel.project_id == project_id).all()
    return team_members




@router.delete("/projects/{project_id}/team/{user_id}")
def remove_team_member(project_id: int, user_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if current user is the project owner
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.ownerId != current_user.id:
        raise HTTPException(status_code=403, detail="Only project owner can remove team members")

    member = db.query(TeamModel).filter(
        TeamModel.project_id == project_id,
        TeamModel.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    db.delete(member)
    db.commit()
    return {"message": "Team member removed"}

@router.get("/projects/{project_id}/team/comments", response_model=list[CommentResponseSchema])
def get_team_comments(project_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if not is_team_member(project_id, current_user.id, db):
        raise HTTPException(status_code=403, detail="Only team members can view comments")
    
    # Get team_id for the project (assuming one team per project, but since team has project_id, get all comments for teams in this project
    # But since team is per user per project, comments are per team member?
    # Wait, the model has team_id, so comments per team entry.
    # To get all comments for the project's team, query comments where team.project_id == project_id
    comments = db.query(CommentModel).join(TeamModel).filter(TeamModel.project_id == project_id).all()
    return comments

@router.post("/projects/{project_id}/team/comments", response_model=CommentResponseSchema)
def add_team_comment(project_id: int, comment: CommentSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if not is_team_member(project_id, current_user.id, db):
        raise HTTPException(status_code=403, detail="Only team members can add comments")
    
    # Get the team entry for the user in this project
    team = db.query(TeamModel).filter(
        TeamModel.project_id == project_id,
        TeamModel.user_id == current_user.id
    ).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team membership not found")
    
    new_comment = CommentModel(
        team_id=team.id,
        user_id=current_user.id,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
