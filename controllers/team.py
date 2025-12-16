from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.team import TeamModel
from serializers.team import TeamSchema, TeamResponseSchema
from database import get_db

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

