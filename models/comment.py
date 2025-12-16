from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel

class CommentModel(BaseModel):
    __tablename__ = "comments"

    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)

    team = relationship("TeamModel", backref="comments")
    user = relationship("UserModel", backref="comments")