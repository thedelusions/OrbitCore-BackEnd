from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class TeamModel(BaseModel):
    __tablename__ = "team"

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String)
    repo_link = Column(String)
    joined_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="teams")
    