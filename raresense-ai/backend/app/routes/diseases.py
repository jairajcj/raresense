"""
RareSense.AI — Disease Database Routes
CRUD for rare disease database (Orphanet/HPO)
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from bson import ObjectId
from typing import Optional

from app.config import mongo

router = APIRouter(prefix="/api/diseases", tags=["Diseases"])


def serialize_doc(doc):
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("")
async def list_diseases(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: str = "name",
    sort_order: int = 1
):
    """List all diseases with pagination, search, and category filtering."""
    query = {}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"orpha_id": {"$regex": search, "$options": "i"}},
            {"synonyms": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]
    
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    
    skip = (page - 1) * limit
    total = await mongo.db.diseases.count_documents(query)
    
    cursor = mongo.db.diseases.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
    diseases = []
    async for doc in cursor:
        diseases.append(serialize_doc(doc))
    
    return {
        "diseases": diseases,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/categories")
async def get_categories():
    """Get all unique disease categories with counts."""
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$project": {"category": "$_id", "count": 1, "_id": 0}}
    ]
    
    categories = []
    async for doc in mongo.db.diseases.aggregate(pipeline):
        categories.append(doc)
    
    return {"categories": categories}


@router.get("/{disease_id}")
async def get_disease(disease_id: str):
    """Get a single disease by orpha_id or _id."""
    disease = await mongo.db.diseases.find_one({"orpha_id": disease_id})
    if not disease:
        try:
            disease = await mongo.db.diseases.find_one({"_id": ObjectId(disease_id)})
        except Exception:
            pass
    
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    
    return serialize_doc(disease)


@router.post("")
async def create_disease(disease_data: dict):
    """Add a new disease to the database."""
    existing = await mongo.db.diseases.find_one({"orpha_id": disease_data.get("orpha_id")})
    if existing:
        raise HTTPException(status_code=400, detail="Disease with this Orphanet ID already exists")
    
    disease_data["created_at"] = datetime.utcnow()
    result = await mongo.db.diseases.insert_one(disease_data)
    disease_data["_id"] = str(result.inserted_id)
    
    return disease_data


@router.get("/{disease_id}/patients")
async def get_patients_with_disease(disease_id: str):
    """Get all patients matched to this disease."""
    cursor = mongo.db.matches.find(
        {"disease_orpha_id": disease_id}
    ).sort("confidence", -1)
    
    matches = []
    async for doc in cursor:
        # Get patient info
        patient = await mongo.db.patients.find_one({"patient_id": doc["patient_id"]})
        match_doc = serialize_doc(doc)
        if patient:
            match_doc["patient_name"] = f"{patient['first_name']} {patient['last_name']}"
        matches.append(match_doc)
    
    return {"disease_id": disease_id, "matches": matches, "count": len(matches)}
