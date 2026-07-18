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
from app.models.patient import PatientCreate, PatientUpdate, ClinicalNoteCreate, ClinicalNoteUpdate, ClinicianResultCreate
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


@router.get("/me/results")
async def get_my_results(user=Depends(get_current_user)):
    """Patient views their clinician-posted results."""
    if not user or user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Not a patient")
    
    patient = await mongo.db.patients.find_one({"user_id": str(user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    cursor = mongo.db.clinician_results.find(
        {"patient_id": patient["patient_id"]}
    ).sort("created_at", -1)
    
    results = []
    async for doc in cursor:
        results.append(serialize_doc(doc))
    
    return {"results": results, "count": len(results)}


@router.get("/me/predictions")
async def get_my_predictions(user=Depends(get_current_user)):
    """Patient views their AI disease-matching predictions."""
    if not user or user.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Not a patient")
    
    patient = await mongo.db.patients.find_one({"user_id": str(user["_id"])})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    patient_id = patient["patient_id"]
    
    # Get match results
    cursor = mongo.db.matches.find({"patient_id": patient_id}).sort("rank", 1)
    matches = []
    async for doc in cursor:
        matches.append(serialize_doc(doc))
    
    # Get symptom summary from clinical notes
    notes_cursor = mongo.db.clinical_notes.find({"patient_id": patient_id})
    all_symptoms = []
    all_diagnoses = []
    all_medications = []
    total_notes = 0
    async for note in notes_cursor:
        total_notes += 1
        entities = note.get("extracted_entities", [])
        for e in entities:
            if e.get("entity_type") == "symptom":
                all_symptoms.append(e)
            elif e.get("entity_type") == "diagnosis":
                all_diagnoses.append(e)
            elif e.get("entity_type") == "medication":
                all_medications.append(e)
    
    # De-duplicate symptoms by normalized_name
    seen = set()
    unique_symptoms = []
    for s in all_symptoms:
        name = s.get("normalized_name", s.get("text", ""))
        if name not in seen:
            seen.add(name)
            unique_symptoms.append(s)
    
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "matches": matches,
        "match_count": len(matches),
        "symptoms_detected": unique_symptoms,
        "symptom_count": len(unique_symptoms),
        "diagnoses_found": all_diagnoses,
        "medications_found": all_medications,
        "total_notes_analyzed": total_notes
    }


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


async def seed_patient_template_data(patient_id: str, template: str):
    """Seed clinical notes, diagnoses, and timeline events from predefined templates."""
    notes = []
    if template == "lupus":
        notes = [
            {
                "note_type": "consultation",
                "specialty": "Rheumatology",
                "physician": "Dr. Sarah Connor",
                "text": "Patient Elena Vasquez presents with severe fatigue, butterfly rash across nose and cheeks, and persistent joint swelling in hands and wrists. Laboratory tests show positive ANA (1:320) and elevated anti-dsDNA antibodies."
            },
            {
                "note_type": "progress_note",
                "specialty": "Rheumatology",
                "physician": "Dr. Sarah Connor",
                "text": "Follow-up visit. Joint pain is partially managed with prednisone, but fatigue remains high. Suspected Systemic Lupus Erythematosus."
            }
        ]
    elif template == "cystic_fibrosis":
        notes = [
            {
                "note_type": "consultation",
                "specialty": "Pulmonology",
                "physician": "Dr. James Carter",
                "text": "Infant patient exhibits chronic cough, thick respiratory mucus, and failure to thrive. Parents report salty skin. Sweat chloride test confirms elevated chloride level (82 mmol/L). Genotyping shows homozygous F508del mutation in the CFTR gene."
            },
            {
                "note_type": "progress_note",
                "specialty": "Pulmonology",
                "physician": "Dr. James Carter",
                "text": "Prescribed dornase alfa and chest physiotherapy to improve airway clearance. Nutrient absorption managed with pancreatic enzyme replacement therapy (PERT)."
            }
        ]
    elif template == "huntington":
        notes = [
            {
                "note_type": "consultation",
                "specialty": "Neurology",
                "physician": "Dr. Allison House",
                "text": "Adult patient presents with involuntary choreic movements of the extremities, progressive cognitive decline, and mood disturbances. Family history positive for autosomal dominant neurological disease. Genetic testing reveals 42 CAG repeats in the HTT gene."
            }
        ]

    for note in notes:
        # Run BioBERT/MedSpacy entity extraction
        entities = extract_entities(note["text"])
        note_id = f"N-{uuid.uuid4().hex[:8].upper()}"
        
        note_doc = {
            "note_id": note_id,
            "patient_id": patient_id,
            "note_type": note["note_type"],
            "specialty": note["specialty"],
            "physician": note["physician"],
            "date": datetime.utcnow(),
            "text": note["text"],
            "extracted_entities": entities,
            "created_at": datetime.utcnow()
        }
        await mongo.db.clinical_notes.insert_one(note_doc)
        
    if notes:
        await mongo.db.patients.update_one(
            {"patient_id": patient_id},
            {"$set": {"notes_count": len(notes), "matches_count": 1}}
        )


@router.post("")
async def create_patient(patient_data: PatientCreate):
    """Create a new patient and optionally seed case files from templates."""
    patient_id = f"P-{uuid.uuid4().hex[:8].upper()}"
    
    doc = patient_data.model_dump()
    doc["patient_id"] = patient_id
    doc["notes_count"] = 0
    doc["matches_count"] = 0
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()
    
    # Remove template parameter before database write
    template = doc.pop("template", None)
    
    result = await mongo.db.patients.insert_one(doc)
    
    # Seed timeline items if template requested
    if template:
        await seed_patient_template_data(patient_id, template)
        
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "patient_created",
        "details": f"Patient {doc['first_name']} {doc['last_name']} ({patient_id}) created" + (f" using template '{template}'" if template else ""),
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
    
    # Generate IDs for reports if they exist
    reports_list = []
    if note_data.reports:
        for report in note_data.reports:
            rep_dict = report.model_dump()
            if not rep_dict.get("report_id"):
                rep_dict["report_id"] = f"R-{uuid.uuid4().hex[:8].upper()}"
            # Ensure uploaded_at exists
            if not rep_dict.get("uploaded_at"):
                rep_dict["uploaded_at"] = datetime.utcnow()
            reports_list.append(rep_dict)
            
    note_doc = {
        "note_id": f"N-{uuid.uuid4().hex[:8].upper()}",
        "patient_id": patient_id,
        "note_type": note_data.note_type,
        "specialty": note_data.specialty,
        "physician": note_data.physician,
        "date": note_data.date,
        "text": note_data.text,
        "extracted_entities": entities,
        "reports": reports_list,
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
        "details": f"Clinical note ({note_data.note_type}) added to patient {patient_id}. Extracted {len(entities)} entities. Attached {len(reports_list)} reports.",
        "entity_type": "clinical_note",
        "entity_id": note_doc["note_id"],
        "timestamp": datetime.utcnow()
    })
    
    note_doc["_id"] = str(result.inserted_id)
    return serialize_doc(note_doc)

@router.put("/notes/{note_id}")
async def update_clinical_note(note_id: str, note_data: ClinicalNoteUpdate):
    """Update a clinical note (timeline event)."""
    update_dict = {k: v for k, v in note_data.model_dump().items() if v is not None}
    
    if "text" in update_dict:
        entities = extract_entities(update_dict["text"])
        update_dict["extracted_entities"] = entities
        
    if "reports" in update_dict and update_dict["reports"] is not None:
        reports_list = []
        for report in update_dict["reports"]:
            # report can be a dict already if Pydantic parsed it, or a Pydantic model
            rep_dict = report if isinstance(report, dict) else report.model_dump()
            if not rep_dict.get("report_id"):
                rep_dict["report_id"] = f"R-{uuid.uuid4().hex[:8].upper()}"
            if not rep_dict.get("uploaded_at"):
                rep_dict["uploaded_at"] = datetime.utcnow()
            reports_list.append(rep_dict)
        update_dict["reports"] = reports_list
        
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
            "text": 1,  # Keep full text for details/editing
            "reports": 1,
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
            "reports": doc.get("reports", []) or [],
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


# ── Clinician-Posted Results ────────────────────────────────────────────

@router.post("/{patient_id}/results")
async def post_clinician_result(
    patient_id: str,
    result_data: ClinicianResultCreate,
    user=Depends(get_current_user)
):
    """Clinician posts a medical result for a specific patient."""
    if not user or user.get("role") not in ("clinician", "admin"):
        raise HTTPException(status_code=403, detail="Only clinicians can post results")
    
    patient = await mongo.db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    result_doc = {
        "result_id": f"R-{uuid.uuid4().hex[:8].upper()}",
        "patient_id": patient_id,
        "result_type": result_data.result_type,
        "title": result_data.title,
        "summary": result_data.summary,
        "severity": result_data.severity,
        "physician": result_data.physician or user.get("full_name", "Unknown"),
        "posted_by": user.get("username", "unknown"),
        "attachments": result_data.attachments or [],
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    
    await mongo.db.clinician_results.insert_one(result_doc)
    result_doc["_id"] = str(result_doc.get("_id", ""))
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "result_posted",
        "user": user.get("username"),
        "details": f"Clinician posted '{result_data.title}' ({result_data.result_type}) for patient {patient_id}",
        "entity_type": "clinician_result",
        "entity_id": result_doc["result_id"],
        "timestamp": datetime.utcnow()
    })
    
    return result_doc


@router.get("/{patient_id}/results")
async def get_patient_results(patient_id: str):
    """Get all clinician-posted results for a patient."""
    cursor = mongo.db.clinician_results.find(
        {"patient_id": patient_id}
    ).sort("created_at", -1)
    
    results = []
    async for doc in cursor:
        results.append(serialize_doc(doc))
    
    return {"results": results, "count": len(results)}


