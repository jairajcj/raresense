"""
RareSense.AI — Patient CRUD Routes
Full CRUD + clinical notes + timeline
"""
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends
from datetime import datetime
from bson import ObjectId
from typing import Optional
import uuid
import asyncio

from app.config import mongo
from app.models.patient import PatientCreate, PatientUpdate, ClinicalNoteCreate, ClinicalNoteUpdate
from app.services.nlp_engine import extract_entities
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/patients", tags=["Patients"])


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("")
async def list_patients(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: int = -1
):
    """List all patients with pagination, search, and filtering."""
    query = {}
    
    if search:
        query["$or"] = [
            {"first_name": {"$regex": search, "$options": "i"}},
            {"last_name": {"$regex": search, "$options": "i"}},
            {"patient_id": {"$regex": search, "$options": "i"}},
        ]
    
    if status:
        query["status"] = status
    
    skip = (page - 1) * limit
    
    total = await mongo.db.patients.count_documents(query)
    cursor = mongo.db.patients.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
    patients = []
    async for doc in cursor:
        patients.append(serialize_doc(doc))
    
    return {
        "patients": patients,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/me")
async def get_my_patient_profile(user=Depends(get_current_user)):
    """Get the patient profile linked to the current logged-in user."""
    if not user or user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Not a patient")
    patient = await mongo.db.patients.find_one({"user_id": str(user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return serialize_doc(patient)

@router.post("/me/upload-prescription")
async def upload_prescription(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    """Mock OCR for prescription image upload."""
    if not user or user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Not a patient")
    patient = await mongo.db.patients.find_one({"user_id": str(user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    # Mock OCR delay
    await asyncio.sleep(2)
    mock_text = f"Extracted from {file.filename}: Patient exhibits signs of fatigue, joint pain, and occasional skin rash. Previous doctors suspected autoimmune disease. Recommended to monitor for lupus-like symptoms. Current medications: Ibuprofen."
    
    # Run NLP extraction
    entities = extract_entities(mock_text)
    
    note_doc = {
        "note_id": f"N-{uuid.uuid4().hex[:8].upper()}",
        "patient_id": patient["patient_id"],
        "note_type": "prescription_upload",
        "specialty": "General",
        "physician": "Uploaded Doctor",
        "date": datetime.utcnow(),
        "text": mock_text,
        "extracted_entities": entities,
        "created_at": datetime.utcnow()
    }
    
    result = await mongo.db.clinical_notes.insert_one(note_doc)
    
    await mongo.db.patients.update_one(
        {"patient_id": patient["patient_id"]},
        {"$inc": {"notes_count": 1}, "$set": {"updated_at": datetime.utcnow()}}
    )
    
    note_doc["_id"] = str(result.inserted_id)
    return {"message": "Prescription analyzed successfully", "note": note_doc}


@router.get("/{patient_id}")
async def get_patient(patient_id: str):
    """Get a single patient by patient_id."""
    patient = await mongo.db.patients.find_one({"patient_id": patient_id})
    if not patient:
        # Try by _id
        try:
            patient = await mongo.db.patients.find_one({"_id": ObjectId(patient_id)})
        except Exception:
            pass
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return serialize_doc(patient)


@router.post("")
async def create_patient(patient_data: PatientCreate):
    """Create a new patient."""
    patient_id = f"P-{uuid.uuid4().hex[:8].upper()}"
    
    doc = patient_data.model_dump()
    doc["patient_id"] = patient_id
    doc["notes_count"] = 0
    doc["matches_count"] = 0
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()
    
    result = await mongo.db.patients.insert_one(doc)
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "patient_created",
        "details": f"Patient {doc['first_name']} {doc['last_name']} ({patient_id}) created",
        "entity_type": "patient",
        "entity_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    doc["_id"] = str(result.inserted_id)
    return doc


@router.put("/{patient_id}")
async def update_patient(patient_id: str, update_data: PatientUpdate):
    """Update a patient's information."""
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    update_dict["updated_at"] = datetime.utcnow()
    
    result = await mongo.db.patients.find_one_and_update(
        {"patient_id": patient_id},
        {"$set": update_dict},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "patient_updated",
        "details": f"Patient {patient_id} updated: {list(update_dict.keys())}",
        "entity_type": "patient",
        "entity_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    return serialize_doc(result)


@router.delete("/{patient_id}")
async def delete_patient(patient_id: str):
    """Delete a patient and all associated data."""
    result = await mongo.db.patients.delete_one({"patient_id": patient_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Delete associated clinical notes and matches
    await mongo.db.clinical_notes.delete_many({"patient_id": patient_id})
    await mongo.db.matches.delete_many({"patient_id": patient_id})
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "patient_deleted",
        "details": f"Patient {patient_id} and associated data deleted",
        "entity_type": "patient",
        "entity_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "Patient deleted successfully", "patient_id": patient_id}


# ── Clinical Notes ──────────────────────────────────────────────────────

@router.get("/{patient_id}/notes")
async def get_patient_notes(patient_id: str, sort_order: int = 1):
    """Get all clinical notes for a patient, sorted chronologically."""
    cursor = mongo.db.clinical_notes.find(
        {"patient_id": patient_id}
    ).sort("date", sort_order)
    
    notes = []
    async for doc in cursor:
        notes.append(serialize_doc(doc))
    
    return {"notes": notes, "count": len(notes)}


@router.post("/{patient_id}/notes")
async def add_clinical_note(patient_id: str, note_data: ClinicalNoteCreate):
    """Add a clinical note to a patient. Automatically runs NLP extraction."""
    # Verify patient exists
    patient = await mongo.db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Run NLP extraction
    entities = extract_entities(note_data.text)
    
    note_doc = {
        "note_id": f"N-{uuid.uuid4().hex[:8].upper()}",
        "patient_id": patient_id,
        "note_type": note_data.note_type,
        "specialty": note_data.specialty,
        "physician": note_data.physician,
        "date": note_data.date,
        "text": note_data.text,
        "extracted_entities": entities,
        "created_at": datetime.utcnow()
    }
    
    result = await mongo.db.clinical_notes.insert_one(note_doc)
    
    # Update patient notes count
    await mongo.db.patients.update_one(
        {"patient_id": patient_id},
        {
            "$inc": {"notes_count": 1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "note_added",
        "details": f"Clinical note ({note_data.note_type}) added to patient {patient_id}. Extracted {len(entities)} entities.",
        "entity_type": "clinical_note",
        "entity_id": note_doc["note_id"],
        "timestamp": datetime.utcnow()
    })
    
    note_doc["_id"] = str(result.inserted_id)
    return note_doc

@router.put("/notes/{note_id}")
async def update_clinical_note(note_id: str, note_data: ClinicalNoteUpdate):
    """Update a clinical note (timeline event)."""
    update_dict = {k: v for k, v in note_data.model_dump().items() if v is not None}
    
    if "text" in update_dict:
        entities = extract_entities(update_dict["text"])
        update_dict["extracted_entities"] = entities
        
    result = await mongo.db.clinical_notes.find_one_and_update(
        {"note_id": note_id},
        {"$set": update_dict},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return serialize_doc(result)

@router.delete("/notes/{note_id}")
async def delete_clinical_note(note_id: str):
    """Delete a clinical note (timeline event)."""
    note = await mongo.db.clinical_notes.find_one({"note_id": note_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    await mongo.db.clinical_notes.delete_one({"note_id": note_id})
    await mongo.db.patients.update_one(
        {"patient_id": note["patient_id"]},
        {"$inc": {"notes_count": -1}}
    )
    return {"message": "Note deleted successfully"}



# ── Patient Timeline ────────────────────────────────────────────────────

@router.get("/{patient_id}/timeline")
async def get_patient_timeline(patient_id: str):
    """
    Build a chronological health timeline for a patient.
    Aggregates all clinical notes, extracts entities, and orders by date.
    """
    # Aggregation pipeline for timeline construction
    pipeline = [
        {"$match": {"patient_id": patient_id}},
        {"$sort": {"date": 1}},
        {"$project": {
            "_id": 0,
            "note_id": 1,
            "date": 1,
            "note_type": 1,
            "specialty": 1,
            "physician": 1,
            "text": {"$substrCP": ["$text", 0, 200]},  # First 200 chars as summary
            "extracted_entities": 1,
            "entity_count": {"$size": {"$ifNull": ["$extracted_entities", []]}}
        }}
    ]
    
    timeline = []
    async for doc in mongo.db.clinical_notes.aggregate(pipeline):
        # Group entities by type
        entities = doc.get("extracted_entities", [])
        symptoms = [e for e in entities if e.get("entity_type") == "symptom"]
        medications = [e for e in entities if e.get("entity_type") == "medication"]
        diagnoses = [e for e in entities if e.get("entity_type") == "diagnosis"]
        labs = [e for e in entities if e.get("entity_type") == "lab_value"]
        
        timeline.append({
            "note_id": doc.get("note_id"),
            "date": doc["date"],
            "note_type": doc.get("note_type", ""),
            "specialty": doc.get("specialty", ""),
            "physician": doc.get("physician", ""),
            "summary": doc.get("text", ""),
            "symptoms": symptoms,
            "medications": medications,
            "diagnoses": diagnoses,
            "lab_values": labs,
            "total_entities": doc.get("entity_count", 0)
        })
    
    # Collect all unique HPO codes across the timeline
    all_hpo = set()
    for entry in timeline:
        for s in entry["symptoms"]:
            if s.get("hpo_code"):
                all_hpo.add(s["hpo_code"])
    
    return {
        "patient_id": patient_id,
        "timeline": timeline,
        "total_visits": len(timeline),
        "unique_symptoms": len(all_hpo),
        "hpo_codes": list(all_hpo)
    }
