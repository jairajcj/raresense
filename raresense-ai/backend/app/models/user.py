"""
RareSense.AI — User / Auth Models
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """A clinician user."""
    user_id: Optional[str] = None
    username: str
    email: str
    full_name: str
    role: str = Field("clinician", description="admin, clinician, researcher, patient")
    specialty: str = ""
    hashed_password: str = ""
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(BaseModel):
    """Schema for registering a new user."""
    username: str
    email: str
    full_name: str
    password: str
    role: str = "patient"
    specialty: str = ""


class UserLogin(BaseModel):
    """Schema for login."""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: dict = {}
