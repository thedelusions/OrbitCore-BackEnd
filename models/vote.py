from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .base import Base


class VoteModel(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    projectId = Column(Integer, ForeignKey('projects.id'), nullable=False)
    voteType = Column(String, nullable=False)  # "upvote" or "downvote"

    __table_args__ = (UniqueConstraint('userId', 'projectId', name='unique_user_project_vote'),)
