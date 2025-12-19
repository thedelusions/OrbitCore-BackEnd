from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.request import RequestModel, RequestStatus
from models.project import ProjectModel
from models.team import TeamModel
from serializers.request import RequestCreateSchema, RequestUpdateSchema, RequestResponseSchema, RequestWithDetailsSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel

router = APIRouter()


@router.post("/projects/{project_id}/requests", response_model=RequestResponseSchema)
def request_to_join_project(project_id: int, request: RequestCreateSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing_request = db.query(RequestModel).filter(
        (RequestModel.project_id == project_id) & (RequestModel.user_id == current_user.id)
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=400, detail="Request already exists for this project")
    
    new_request = RequestModel(
        project_id=project_id,
        user_id=current_user.id,
        message=request.message,
        status=RequestStatus.PENDING
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return new_request


@router.get("/projects/{project_id}/requests", response_model=List[RequestWithDetailsSchema])
def get_project_requests(project_id: int, db: Session = Depends(get_db)):

    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    requests = db.query(RequestModel).filter(RequestModel.project_id == project_id).all()
    return requests


@router.put("/requests/{request_id}", response_model=RequestResponseSchema)
def accept_or_reject_request(request_id: int, request_update: RequestUpdateSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

    join_request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    
    if not join_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    
    project = db.query(ProjectModel).filter(ProjectModel.id == join_request.project_id).first()
    if project.ownerId != current_user.id:
        raise HTTPException(status_code=403, detail="Only project owner can manage requests")

    if join_request.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Request already handled")

    if request_update.status == RequestStatus.ACCEPTED.value:
        join_request.status = RequestStatus.ACCEPTED

       
        team_member = TeamModel(
            project_id=join_request.project_id,
            user_id=join_request.user_id,
            role="Member"
        )
        db.add(team_member)

    elif request_update.status == RequestStatus.REJECTED.value:
        join_request.status = RequestStatus.REJECTED

    else:
        raise HTTPException(status_code=400, detail="Invalid status")

    db.commit()
    db.refresh(join_request)
    return join_request

@router.get("/users/me/requests", response_model=List[RequestWithDetailsSchema])
def get_my_join_requests(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):

    requests = db.query(RequestModel).filter(RequestModel.user_id == current_user.id).all()
    return requests
