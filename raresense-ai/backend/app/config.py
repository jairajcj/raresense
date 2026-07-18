"""
RareSense.AI — MongoDB Atlas Configuration
Connects to MongoDB Atlas cloud cluster via environment variables
"""
import os
import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = os.getenv("DATABASE_NAME", "raresense")

# Async client for FastAPI (uses certifi for Atlas TLS)
class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB Atlas on startup."""
    mongo.client = AsyncIOMotorClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    mongo.db = mongo.client[DATABASE_NAME]
    # Verify connection
    try:
        await mongo.client.admin.command("ping")
        print(f"[OK] Connected to MongoDB Atlas: {DATABASE_NAME}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB Atlas: {e}")
        raise e
    # Create indexes
    await create_indexes()

async def close_mongo_connection():
    """Close MongoDB connection on shutdown."""
    if mongo.client:
        mongo.client.close()
        print("[INFO] MongoDB Atlas connection closed")

async def create_indexes():
    """Create all required indexes for the database."""
    db = mongo.db
    
    try:
        # Text index on clinical notes for full-text search
        await db.clinical_notes.create_index([
            ("text", "text"),
            ("note_type", "text")
        ], name="clinical_notes_text_idx")
    except Exception as e:
        # Index may already exist with different options — skip
        print(f"[WARNING] clinical_notes text index: {e}")
    
    try:
        # Compound index on patients
        await db.patients.create_index([
            ("last_name", 1),
            ("first_name", 1)
        ], name="patients_name_idx")
    except Exception:
        pass
    
    try:
        await db.patients.create_index("patient_id", unique=True, name="patients_id_idx")
    except Exception:
        pass
    
    try:
        # Index on clinical notes by patient
        await db.clinical_notes.create_index("patient_id", name="notes_patient_idx")
        await db.clinical_notes.create_index("date", name="notes_date_idx")
    except Exception:
        pass
    
    try:
        # Index on diseases
        await db.diseases.create_index("orpha_id", unique=True, name="diseases_orpha_idx")
        await db.diseases.create_index([("name", "text")], name="diseases_text_idx")
    except Exception as e:
        print(f"[WARNING] diseases index: {e}")
    
    try:
        # Index on matches
        await db.matches.create_index("patient_id", name="matches_patient_idx")
        await db.matches.create_index([("confidence", -1)], name="matches_confidence_idx")
    except Exception:
        pass
    
    try:
        # Index on activity logs
        await db.activity_logs.create_index([("timestamp", -1)], name="logs_time_idx")
        await db.activity_logs.create_index("action", name="logs_action_idx")
    except Exception:
        pass
    
    try:
        # TTL index on OTP codes (auto-expire after 10 minutes)
        await db.otp_codes.create_index("created_at", expireAfterSeconds=600, name="otp_ttl_idx")
    except Exception:
        pass
    
    print("[INFO] Database indexes created")

def get_sync_db():
    """Get synchronous MongoDB connection for seeding (uses Atlas URI)."""
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    return client[DATABASE_NAME]
