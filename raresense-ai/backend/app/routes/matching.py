"""
RareSense.AI — Disease Matching Routes (Week 4)
Run phenotype matching engine on patients
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
import uuid

from app.config import mongo
from app.services.nlp_engine import extract_entities, get_patient_phenotype
from app.services.matcher import match_patient_to_diseases

router = APIRouter(prefix="/api/match", tags=["Matching Engine"])


def serialize_doc(doc):
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


@router.post("/{patient_id}")
async def run_matching(patient_id: str, top_k: int = 10):
    """
    Run the rare disease matching engine on a patient.
    1. Collects all clinical notes for the patient
    2. Extracts all HPO phenotype codes
    3. Matches against the disease database using cosine similarity
    4. Stores match results in MongoDB
    """
    # Verify patient exists
    patient = await mongo.db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get all clinical notes for the patient
    notes_cursor = mongo.db.clinical_notes.find({"patient_id": patient_id})
    all_entities = []
    all_entity_lists = []
    
    async for note in notes_cursor:
        entities = note.get("extracted_entities", [])
        all_entities.extend(entities)
        all_entity_lists.append(entities)
    
    if not all_entities:
        raise HTTPException(
            status_code=400,
            detail="No clinical notes or extracted entities found for this patient. Add clinical notes first."
        )
    
    # Get patient phenotype (unique HPO codes)
    patient_hpo = get_patient_phenotype(all_entity_lists)
    
    if not patient_hpo:
        raise HTTPException(
            status_code=400,
            detail="No symptoms with HPO codes found in patient's clinical notes."
        )
    
    # Get all diseases from database
    diseases = []
    async for disease in mongo.db.diseases.find():
        disease["_id"] = str(disease["_id"])
        diseases.append(disease)
    
    # Run matching engine
    matches = match_patient_to_diseases(
        patient_hpo_codes=patient_hpo,
        diseases=diseases,
        patient_entities=all_entities,
        top_k=top_k
    )
    
    # Delete previous matches for this patient
    await mongo.db.matches.delete_many({"patient_id": patient_id})
    
    # Store match results
    stored_matches = []
    for match in matches:
        match_doc = {
            "match_id": f"M-{uuid.uuid4().hex[:8].upper()}",
            "patient_id": patient_id,
            "disease_orpha_id": match["disease_orpha_id"],
            "disease_name": match["disease_name"],
            "confidence": match["confidence"],
            "matched_symptoms": match["matched_symptoms"],
            "total_disease_symptoms": match["total_disease_symptoms"],
            "matched_count": match["matched_count"],
            "rank": match["rank"],
            "status": "pending",
            "created_at": datetime.utcnow()
        }
        await mongo.db.matches.insert_one(match_doc)
        match_doc["_id"] = str(match_doc.get("_id", ""))
        stored_matches.append(match_doc)
    
    # Update patient matches count
    await mongo.db.patients.update_one(
        {"patient_id": patient_id},
        {"$set": {"matches_count": len(stored_matches), "updated_at": datetime.utcnow()}}
    )
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "match_run",
        "details": f"Matching engine run on patient {patient_id}: {len(patient_hpo)} phenotypes matched against {len(diseases)} diseases. Top match: {matches[0]['disease_name'] if matches else 'None'} ({round(matches[0]['confidence']*100, 1)}%)" if matches else f"No matches found for {patient_id}",
        "entity_type": "match",
        "entity_id": patient_id,
        "timestamp": datetime.utcnow()
    })
    
    return {
        "patient_id": patient_id,
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "phenotype_count": len(patient_hpo),
        "hpo_codes": patient_hpo,
        "diseases_searched": len(diseases),
        "matches": stored_matches
    }


@router.get("/{patient_id}/results")
async def get_match_results(patient_id: str):
    """Get stored match results for a patient."""
    cursor = mongo.db.matches.find(
        {"patient_id": patient_id}
    ).sort("rank", 1)
    
    matches = []
    async for doc in cursor:
        matches.append(serialize_doc(doc))
    
    patient = await mongo.db.patients.find_one({"patient_id": patient_id})
    patient_name = f"{patient['first_name']} {patient['last_name']}" if patient else patient_id
    
    return {
        "patient_id": patient_id,
        "patient_name": patient_name,
        "matches": matches,
        "count": len(matches)
    }


@router.put("/{match_id}/status")
async def update_match_status(match_id: str, body: dict):
    """Update the status of a disease match (confirm, dismiss, under_review)."""
    new_status = body.get("status", "pending")
    notes = body.get("notes", "")
    
    result = await mongo.db.matches.find_one_and_update(
        {"match_id": match_id},
        {"$set": {"status": new_status, "notes": notes}},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Log activity
    await mongo.db.activity_logs.insert_one({
        "action": "match_status_updated",
        "details": f"Match {match_id} status changed to {new_status}",
        "entity_type": "match",
        "entity_id": match_id,
        "timestamp": datetime.utcnow()
    })
    
    return serialize_doc(result)


@router.post("/analyze-note")
async def analyze_single_note(body: dict):
    """Analyze a single clinical note and find matching diseases."""
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No clinical text provided")
    
    # Extract entities
    entities = extract_entities(text)
    hpo_codes = [e["hpo_code"] for e in entities if e.get("hpo_code")]
    
    if not hpo_codes:
        return {
            "entities": entities,
            "matches": [],
            "message": "No symptoms with HPO codes found in the text"
        }
    
    # Get diseases
    diseases = []
    async for disease in mongo.db.diseases.find():
        disease["_id"] = str(disease["_id"])
        diseases.append(disease)
    
    # Run matching
    matches = match_patient_to_diseases(
        patient_hpo_codes=hpo_codes,
        diseases=diseases,
        patient_entities=entities,
        top_k=5
    )
    
    return {
        "text": text,
        "entities": entities,
        "hpo_codes": hpo_codes,
        "matches": matches
    }
