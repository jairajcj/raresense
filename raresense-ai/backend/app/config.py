"""
RareSense.AI — MongoDB Configuration
Connects to local MongoDB instance
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "raresense"

# Async client for FastAPI
class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongo = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB on startup."""
    mongo.client = AsyncIOMotorClient(MONGO_URI)
    mongo.db = mongo.client[DATABASE_NAME]
    # Create indexes
    await create_indexes()
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")

async def close_mongo_connection():
    """Close MongoDB connection on shutdown."""
    if mongo.client:
        mongo.client.close()
        print("❌ MongoDB connection closed")

async def create_indexes():
    """Create all required indexes for the database."""
    db = mongo.db
    
    # Text index on clinical notes for full-text search
    await db.clinical_notes.create_index([
        ("text", "text"),
        ("note_type", "text")
    ], name="clinical_notes_text_idx")
    
    # Compound index on patients
    await db.patients.create_index([
        ("last_name", 1),
        ("first_name", 1)
    ], name="patients_name_idx")
    
    await db.patients.create_index("patient_id", unique=True, name="patients_id_idx")
    
    # Index on clinical notes by patient
    await db.clinical_notes.create_index("patient_id", name="notes_patient_idx")
    await db.clinical_notes.create_index("date", name="notes_date_idx")
    
    # Index on diseases
    await db.diseases.create_index("orpha_id", unique=True, name="diseases_orpha_idx")
    await db.diseases.create_index([("name", "text")], name="diseases_text_idx")
    
    # Index on matches
    await db.matches.create_index("patient_id", name="matches_patient_idx")
    await db.matches.create_index([("confidence", -1)], name="matches_confidence_idx")
    
    # Index on activity logs
    await db.activity_logs.create_index([("timestamp", -1)], name="logs_time_idx")
    await db.activity_logs.create_index("action", name="logs_action_idx")
    
    print("📇 Database indexes created")

def get_sync_db():
    """Get synchronous MongoDB connection for seeding."""
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]
