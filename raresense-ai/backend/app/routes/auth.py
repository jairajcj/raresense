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

import os
from app.config import mongo
from app.models.user import UserCreate, UserLogin, Token, ClinicianLoginRequest, OTPRequest, OTPVerifyRequest
import uuid
import random

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "raresense-ai-secret-key-2026-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
CLINICIAN_INSTITUTIONAL_CODE = os.getenv("CLINICIAN_INSTITUTIONAL_CODE", "RARESENSE2026")

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


@router.get("/google-config")
async def get_google_config():
    """Get the active Google Client ID from environment variables."""
    import os
    client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    return {"client_id": client_id}


# ── Clinician Institutional Code Login ──────────────────────────────────

@router.post("/clinician-login")
async def clinician_login(data: ClinicianLoginRequest):
    """Login as clinician using institutional access code."""
    if data.institutional_code != CLINICIAN_INSTITUTIONAL_CODE:
        raise HTTPException(status_code=401, detail="Invalid institutional access code")
    
    # Find or create clinician user by email
    user = await mongo.db.users.find_one({"email": data.email})
    if not user:
        username = data.email.split("@")[0]
        existing_username = await mongo.db.users.find_one({"username": username})
        if existing_username:
            username = f"{username}_{uuid.uuid4().hex[:4]}"
        
        full_name = data.full_name or username
        user_doc = {
            "username": username,
            "email": data.email,
            "full_name": full_name,
            "role": "clinician",
            "specialty": "General",
            "hashed_password": pwd_context.hash(uuid.uuid4().hex),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await mongo.db.users.insert_one(user_doc)
        user = await mongo.db.users.find_one({"_id": result.inserted_id})
    else:
        # Ensure role is clinician
        if user.get("role") != "clinician":
            await mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"role": "clinician", "specialty": user.get("specialty") or "General"}}
            )
            user["role"] = "clinician"
    
    token = create_token({"sub": user["username"], "role": "clinician"})
    
    await mongo.db.activity_logs.insert_one({
        "action": "clinician_login",
        "user": user["username"],
        "details": f"Clinician {user['full_name']} logged in via institutional code",
        "timestamp": datetime.utcnow()
    })
    
    return {
        "access_token": token,
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": "clinician",
            "specialty": user.get("specialty", "")
        }
    }


# ── Email OTP Login ─────────────────────────────────────────────────────

@router.post("/send-otp")
async def send_otp(data: OTPRequest):
    """Generate and store a 6-digit OTP for email-based clinician login."""
    otp_code = str(random.randint(100000, 999999))
    
    # Store OTP in MongoDB (upsert by email, auto-expire after 10 min)
    await mongo.db.otp_codes.update_one(
        {"email": data.email},
        {
            "$set": {
                "email": data.email,
                "code": otp_code,
                "created_at": datetime.utcnow()
            }
        },
        upsert=True
    )
    
    # In dev mode, return the OTP directly (no email service needed)
    # In production, integrate SendGrid/SES here and remove the otp_code from response
    return {
        "message": f"OTP sent to {data.email}",
        "otp_code": otp_code  # DEV ONLY — remove in production
    }


@router.post("/verify-otp")
async def verify_otp(data: OTPVerifyRequest):
    """Verify OTP code and issue a clinician JWT."""
    record = await mongo.db.otp_codes.find_one({"email": data.email})
    if not record:
        raise HTTPException(status_code=401, detail="No OTP found for this email. Please request a new code.")
    
    # Check expiry (10 minutes)
    age = (datetime.utcnow() - record["created_at"]).total_seconds()
    if age > 600:
        await mongo.db.otp_codes.delete_one({"email": data.email})
        raise HTTPException(status_code=401, detail="OTP has expired. Please request a new code.")
    
    if record["code"] != data.otp_code:
        raise HTTPException(status_code=401, detail="Invalid OTP code")
    
    # OTP valid — delete it
    await mongo.db.otp_codes.delete_one({"email": data.email})
    
    # Find or create clinician user
    user = await mongo.db.users.find_one({"email": data.email})
    if not user:
        username = data.email.split("@")[0]
        existing_username = await mongo.db.users.find_one({"username": username})
        if existing_username:
            username = f"{username}_{uuid.uuid4().hex[:4]}"
        
        user_doc = {
            "username": username,
            "email": data.email,
            "full_name": username,
            "role": "clinician",
            "specialty": "General",
            "hashed_password": pwd_context.hash(uuid.uuid4().hex),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await mongo.db.users.insert_one(user_doc)
        user = await mongo.db.users.find_one({"_id": result.inserted_id})
    else:
        if user.get("role") != "clinician":
            await mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"role": "clinician"}}
            )
            user["role"] = "clinician"
    
    token = create_token({"sub": user["username"], "role": "clinician"})
    
    await mongo.db.activity_logs.insert_one({
        "action": "clinician_otp_login",
        "user": user["username"],
        "details": f"Clinician {user['full_name']} logged in via email OTP",
        "timestamp": datetime.utcnow()
    })
    
    return {
        "access_token": token,
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": "clinician",
            "specialty": user.get("specialty", "")
        }
    }


from pydantic import BaseModel

class GoogleLoginRequest(BaseModel):
    token: str
    email: str
    name: str
    role: str = "patient"

@router.post("/google-login")
async def google_login(data: GoogleLoginRequest):
    """Exchange Google token for backend session token."""
    email = data.email
    name = data.name
    role = "patient"  # Google login is restricted to patient portal only
    
    # 1. Find or create user account
    user = await mongo.db.users.find_one({"email": email})
    if not user:
        username = email.split("@")[0]
        existing_username = await mongo.db.users.find_one({"username": username})
        if existing_username:
            username = f"{username}_{uuid.uuid4().hex[:4]}"
            
        user_doc = {
            "username": username,
            "email": email,
            "full_name": name,
            "role": role,
            "specialty": "Genetics" if role == "clinician" else "",
            "hashed_password": pwd_context.hash(uuid.uuid4().hex),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        result = await mongo.db.users.insert_one(user_doc)
        user = await mongo.db.users.find_one({"_id": result.inserted_id})
    else:
        # Ensure Google login always sets role to patient
        if user.get("role") != "patient":
            await mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"role": "patient", "specialty": ""}}
            )
            user["role"] = "patient"
    
    # 2. Handle patient profile linking
    patient = await mongo.db.patients.find_one({"user_id": str(user["_id"])})
    if not patient:
        # Check if there is an existing case study patient we can link to (e.g. Elena Vasquez)
        if "elena" in name.lower() or "vasquez" in name.lower() or "elena.vasquez" in email.lower():
            existing_lupus = await mongo.db.patients.find_one({"patient_id": "P-LUPUS001"})
            if existing_lupus:
                await mongo.db.patients.update_one(
                    {"patient_id": "P-LUPUS001"},
                    {"$set": {"user_id": str(user["_id"])}}
                )
                patient = existing_lupus
        
        if not patient:
            # Create a new patient profile
            patient_id = f"P-{uuid.uuid4().hex[:8].upper()}"
            names = name.split()
            first = names[0] if names else ""
            last = " ".join(names[1:]) if len(names) > 1 else ""
            patient_doc = {
                "patient_id": patient_id,
                "user_id": str(user["_id"]),
                "first_name": first,
                "last_name": last,
                "date_of_birth": datetime.utcnow() - timedelta(days=365*28),
                "gender": "F" if "elena" in name.lower() else "M",
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
    
    # 3. Create backend JWT token (always patient for Google login)
    token = create_token({"sub": user["username"], "role": "patient"})
    
    return {
        "access_token": token,
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": "patient",
            "specialty": ""
        }
    }
