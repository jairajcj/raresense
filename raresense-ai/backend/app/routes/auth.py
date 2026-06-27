"""
RareSense.AI — Authentication Routes
JWT-based auth with bcrypt password hashing
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from bson import ObjectId

from app.config import mongo
from app.models.user import UserCreate, UserLogin, Token
import uuid

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

SECRET_KEY = "raresense-ai-secret-key-2026-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get the current authenticated user."""
    if not credentials:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        user = await mongo.db.users.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except JWTError:
        return None


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new clinician user."""
    # Check existing
    existing = await mongo.db.users.find_one({
        "$or": [
            {"username": user_data.username},
            {"email": user_data.email}
        ]
    })
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed = pwd_context.hash(user_data.password)
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "specialty": user_data.specialty,
        "hashed_password": hashed,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    result = await mongo.db.users.insert_one(user_doc)
    user_id_str = str(result.inserted_id)
    
    if user_data.role == "patient":
        patient_id = f"P-{uuid.uuid4().hex[:8].upper()}"
        names = user_data.full_name.split()
        first = names[0] if names else ""
        last = " ".join(names[1:]) if len(names) > 1 else ""
        patient_doc = {
            "patient_id": patient_id,
            "user_id": user_id_str,
            "first_name": first,
            "last_name": last,
            "date_of_birth": datetime.utcnow(),
            "gender": "Other",
            "medical_history": [],
            "current_medications": [],
            "allergies": [],
            "status": "active",
            "notes_count": 0,
            "matches_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await mongo.db.patients.insert_one(patient_doc)
    
    token = create_token({"sub": user_data.username, "role": user_data.role})
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "user_registered",
        "user": user_data.username,
        "details": f"New {user_data.role} registered: {user_data.full_name}",
        "timestamp": datetime.utcnow()
    })
    
    return Token(
        access_token=token,
        user={
            "id": str(result.inserted_id),
            "username": user_data.username,
            "full_name": user_data.full_name,
            "email": user_data.email,
            "role": user_data.role,
            "specialty": user_data.specialty
        }
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login with username/password."""
    user = await mongo.db.users.find_one({"username": credentials.username})
    
    if not user or not pwd_context.verify(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    token = create_token({"sub": user["username"], "role": user.get("role", "clinician")})
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "user_login",
        "user": user["username"],
        "details": f"{user['full_name']} logged in",
        "timestamp": datetime.utcnow()
    })
    
    return Token(
        access_token=token,
        user={
            "id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user.get("role", "clinician"),
            "specialty": user.get("specialty", "")
        }
    )


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    """Get current user profile."""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user.pop("hashed_password", None)
    return user
