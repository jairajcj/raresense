"""
RareSense.AI — Search Routes (Week 3)
Full-text search + advanced filtering using MongoDB text indexes
"""
from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional, List

from app.config import mongo
from app.services.nlp_engine import extract_entities

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("")
async def search_clinical_notes(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Full-text search across clinical notes using MongoDB $text index."""
    skip = (page - 1) * limit
    
    # Use MongoDB text search
    query = {"$text": {"$search": q}}
    
    total = await mongo.db.clinical_notes.count_documents(query)
    
    cursor = mongo.db.clinical_notes.find(
        query,
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).skip(skip).limit(limit)
    
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        # Get patient name
        patient = await mongo.db.patients.find_one({"patient_id": doc.get("patient_id")})
        if patient:
            doc["patient_name"] = f"{patient['first_name']} {patient['last_name']}"
        results.append(doc)
    
    # Log search activity
    await mongo.db.activity_logs.insert_one({
        "action": "search_performed",
        "details": f"Search: '{q}' returned {total} results",
        "timestamp": datetime.utcnow()
    })
    
    return {
        "results": results,
        "total": total,
        "query": q,
        "page": page,
        "pages": (total + limit - 1) // limit
    }


@router.get("/filter")
async def filter_notes(
    patient_id: Optional[str] = None,
    specialty: Optional[str] = None,
    note_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    symptom: Optional[str] = None,
    hpo_code: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Advanced filtering on clinical notes with multiple criteria."""
    query = {}
    
    if patient_id:
        query["patient_id"] = patient_id
    
    if specialty:
        query["specialty"] = {"$regex": specialty, "$options": "i"}
    
    if note_type:
        query["note_type"] = note_type
    
    if date_from or date_to:
        date_query = {}
        if date_from:
            date_query["$gte"] = datetime.fromisoformat(date_from)
        if date_to:
            date_query["$lte"] = datetime.fromisoformat(date_to)
        query["date"] = date_query
    
    if symptom:
        query["extracted_entities"] = {
            "$elemMatch": {
                "entity_type": "symptom",
                "normalized_name": {"$regex": symptom, "$options": "i"}
            }
        }
    
    if hpo_code:
        query["extracted_entities.hpo_code"] = hpo_code
    
    skip = (page - 1) * limit
    total = await mongo.db.clinical_notes.count_documents(query)
    
    cursor = mongo.db.clinical_notes.find(query).sort("date", -1).skip(skip).limit(limit)
    
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        patient = await mongo.db.patients.find_one({"patient_id": doc.get("patient_id")})
        if patient:
            doc["patient_name"] = f"{patient['first_name']} {patient['last_name']}"
        results.append(doc)
    
    return {
        "results": results,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit
    }


@router.post("/analyze")
async def analyze_text(body: dict):
    """Analyze arbitrary clinical text and extract entities (NLP demo endpoint)."""
    text = body.get("text", "")
    if not text:
        return {"entities": [], "error": "No text provided"}
    
    entities = extract_entities(text)
    
    # Group by type
    symptoms = [e for e in entities if e["entity_type"] == "symptom"]
    medications = [e for e in entities if e["entity_type"] == "medication"]
    diagnoses = [e for e in entities if e["entity_type"] == "diagnosis"]
    lab_values = [e for e in entities if e["entity_type"] == "lab_value"]
    
    return {
        "text": text,
        "entities": entities,
        "summary": {
            "total": len(entities),
            "symptoms": len(symptoms),
            "medications": len(medications),
            "diagnoses": len(diagnoses),
            "lab_values": len(lab_values)
        },
        "symptoms": symptoms,
        "medications": medications,
        "diagnoses": diagnoses,
        "lab_values": lab_values,
        "hpo_codes": [e["hpo_code"] for e in symptoms if e.get("hpo_code")]
    }


@router.get("/specialties")
async def get_specialties():
    """Get all unique specialties from clinical notes."""
    pipeline = [
        {"$group": {"_id": "$specialty", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$project": {"specialty": "$_id", "count": 1, "_id": 0}}
    ]
    
    specialties = []
    async for doc in mongo.db.clinical_notes.aggregate(pipeline):
        specialties.append(doc)
    
    return {"specialties": specialties}
