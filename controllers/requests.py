from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.request import RequestModel, RequestStatus
from models.project import ProjectModel
from serializers.request import RequestCreateSchema, RequestUpdateSchema, RequestResponseSchema, RequestWithDetailsSchema
from database import get_db

router = APIRouter()


@router.post("/projects/{project_id}/requests", response_model=RequestResponseSchema)
def request_to_join_project(project_id: int, request: RequestCreateSchema, db: Session = Depends(get_db)):

    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing_request = db.query(RequestModel).filter(
        (RequestModel.project_id == project_id) & (RequestModel.user_id == request.user_id)
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=400, detail="Request already exists for this project")
    
    new_request = RequestModel(
        project_id=project_id,
        user_id=request.user_id,
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
def accept_or_reject_request(request_id: int, request_update: RequestUpdateSchema, db: Session = Depends(get_db)):

    join_request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    
    if not join_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    valid_statuses = [RequestStatus.ACCEPTED.value, RequestStatus.REJECTED.value]
    if request_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    
    join_request.status = request_update.status
    
    db.commit()
    db.refresh(join_request)
    
    return join_request


@router.get("/users/me/requests", response_model=List[RequestWithDetailsSchema])
def get_my_join_requests(user_id: int, db: Session = Depends(get_db)):

    requests = db.query(RequestModel).filter(RequestModel.user_id == user_id).all()
    return requests
