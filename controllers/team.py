from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.team import TeamModel
from models.user import UserModel
from models.project import ProjectModel
from serializers.team import TeamSchema, TeamResponseSchema
from database import get_db
from dependencies.get_current_user import get_current_user


router = APIRouter()


@router.get("/projects/{project_id}/team", response_model=list[TeamResponseSchema])
def get_team_members(project_id: int, db: Session = Depends(get_db)):
    team_members = db.query(TeamModel).filter(TeamModel.project_id == project_id).all()
    return team_members

@router.post("/projects/{project_id}/team", response_model=TeamResponseSchema)
def add_team_member(project_id: int, team: TeamSchema, db: Session = Depends(get_db)):
    # Check if user is already in the team
    existing = db.query(TeamModel).filter(
        TeamModel.project_id == project_id,
        TeamModel.user_id == team.user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already in the team")

    new_member = TeamModel(
        project_id=project_id,
        user_id=team.user_id,
        role=team.role,
        repo_link=team.repo_link
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


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
