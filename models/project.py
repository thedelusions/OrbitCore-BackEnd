from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from .base import Base
from datetime import datetime, timezone, timedelta
import enum


class ProjectStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class ProjectTag(str, enum.Enum):
    WEB = "Web"
    MOBILE = "Mobile"
    DESKTOP = "Desktop"
    AI = "AI"
    MACHINE_LEARNING = "Machine Learning"
    DATA_SCIENCE = "Data Science"
    BLOCKCHAIN = "Blockchain"
    IOT = "IoT"
    CLOUD = "Cloud"
    DEVOPS = "DevOps"
    SECURITY = "Security"
    GAME_DEV = "Game Development"
    AR_VR = "AR/VR"
    ECOMMERCE = "E-commerce"
    SOCIAL_MEDIA = "Social Media"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    PRODUCTIVITY = "Productivity"
    API = "API"
    MICROSERVICES = "Microservices"
    FULL_STACK = "Full Stack"
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    DATABASE = "Database"
    ANALYTICS = "Analytics"
    AUTOMATION = "Automation"
    CMS = "CMS"
    SAAS = "SaaS"
    OPEN_SOURCE = "Open Source"
    ENTERPRISE = "Enterprise"
    STARTUP = "Startup"
    PWA = "PWA"
    REAL_TIME = "Real-time"
    CHATBOT = "Chatbot"
    COMPUTER_VISION = "Computer Vision"
    NLP = "NLP"
    DEEP_LEARNING = "Deep Learning"
    BIG_DATA = "Big Data"


class ProjectModel(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ownerId = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.OPEN)
    tags = Column(String, nullable=False)
    upvotes = Column(Integer, default=0, nullable=False)
    downvotes = Column(Integer, default=0, nullable=False)
    
    createdAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False) 