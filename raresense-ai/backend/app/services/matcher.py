"""
RareSense.AI — Rare Disease Phenotype Matching Engine
Cosine similarity between patient symptom vectors and disease profiles.
Simulates MongoDB Vector Search for the prototype.
"""
import math
from typing import List, Dict, Optional


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def build_symptom_vector(hpo_codes: List[str], all_hpo_codes: List[str]) -> List[float]:
    """Build a binary vector from a list of HPO codes against a master vocabulary."""
    hpo_set = set(hpo_codes)
    return [1.0 if code in hpo_set else 0.0 for code in all_hpo_codes]


def match_patient_to_diseases(
    patient_hpo_codes: List[str],
    diseases: List[Dict],
    patient_entities: Optional[List[Dict]] = None,
    top_k: int = 10
) -> List[Dict]:
    """
    Match a patient's phenotype against disease symptom profiles.
    
    Args:
        patient_hpo_codes: List of HPO codes extracted from patient's clinical notes
        diseases: List of disease documents from MongoDB
        patient_entities: Optional list of extracted entities for source text
        top_k: Number of top matches to return
    
    Returns:
        List of disease match results ranked by confidence
    """
    if not patient_hpo_codes or not diseases:
        return []
    
    # Build master HPO vocabulary from all diseases + patient
    all_hpo = set(patient_hpo_codes)
    for disease in diseases:
        for symptom in disease.get("symptoms", []):
            all_hpo.add(symptom["hpo_code"])
    all_hpo_list = sorted(list(all_hpo))
    
    # Build patient vector
    patient_vector = build_symptom_vector(patient_hpo_codes, all_hpo_list)
    
    # Build entity lookup for matched symptom details
    entity_lookup = {}
    if patient_entities:
        for entity in patient_entities:
            if entity.get("hpo_code"):
                entity_lookup[entity["hpo_code"]] = entity
    
    matches = []
    
    for disease in diseases:
        disease_hpo_codes = [s["hpo_code"] for s in disease.get("symptoms", [])]
        if not disease_hpo_codes:
            continue
        
        disease_vector = build_symptom_vector(disease_hpo_codes, all_hpo_list)
        
        # Cosine similarity
        similarity = cosine_similarity(patient_vector, disease_vector)
        
        # Also compute Jaccard-like overlap for interpretability
        patient_set = set(patient_hpo_codes)
        disease_set = set(disease_hpo_codes)
        overlap = patient_set & disease_set
        
        if not overlap:
            continue
        
        # Weighted confidence: combine cosine similarity with overlap ratio
        overlap_ratio = len(overlap) / len(disease_set) if disease_set else 0
        confidence = 0.6 * similarity + 0.4 * overlap_ratio
        
        # Build matched symptoms detail
        matched_symptoms = []
        for hpo in overlap:
            symptom_info = next(
                (s for s in disease.get("symptoms", []) if s["hpo_code"] == hpo),
                {"hpo_code": hpo, "name": hpo}
            )
            entity_info = entity_lookup.get(hpo, {})
            matched_symptoms.append({
                "hpo_code": hpo,
                "symptom_name": symptom_info.get("name", hpo),
                "source_text": entity_info.get("text", ""),
                "note_date": entity_info.get("note_date", ""),
                "specialty": entity_info.get("specialty", "")
            })
        
        matches.append({
            "disease_orpha_id": disease.get("orpha_id", ""),
            "disease_name": disease.get("name", "Unknown"),
            "confidence": round(confidence, 4),
            "matched_symptoms": matched_symptoms,
            "total_disease_symptoms": len(disease_set),
            "matched_count": len(overlap),
            "category": disease.get("category", ""),
        })
    
    # Sort by confidence descending
    matches.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Assign ranks
    for i, match in enumerate(matches[:top_k]):
        match["rank"] = i + 1
    
    return matches[:top_k]
