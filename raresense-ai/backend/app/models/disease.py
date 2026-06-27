"""
RareSense.AI — Pydantic Models for Diseases & Matching
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DiseaseSymptom(BaseModel):
    """A symptom associated with a rare disease."""
    hpo_code: str = Field(..., description="HPO code e.g. HP:0000958")
    name: str = Field(..., description="Human-readable symptom name")
    frequency: str = Field("unknown", description="very_frequent, frequent, occasional, rare")


class RareDisease(BaseModel):
    """A rare disease from the Orphanet/HPO database."""
    disease_id: Optional[str] = None
    orpha_id: str = Field(..., description="Orphanet ID e.g. ORPHA:536")
    name: str
    description: str = ""
    category: str = Field("", description="Disease category/system")
    prevalence: str = Field("unknown", description="Prevalence classification")
    inheritance: str = Field("unknown", description="Inheritance pattern")
    age_of_onset: str = Field("unknown", description="Typical age of onset")
    symptoms: List[DiseaseSymptom] = []
    gene_associations: List[str] = []
    synonyms: List[str] = []


class MatchedSymptom(BaseModel):
    """A symptom that matched between patient and disease."""
    hpo_code: str
    symptom_name: str
    source_text: str = ""
    note_date: Optional[str] = None
    specialty: str = ""


class DiseaseMatch(BaseModel):
    """A rare disease match result for a patient."""
    match_id: Optional[str] = None
    patient_id: str
    disease_orpha_id: str
    disease_name: str
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    matched_symptoms: List[MatchedSymptom] = []
    total_disease_symptoms: int = 0
    matched_count: int = 0
    rank: int = 0
    status: str = Field("pending", description="pending, confirmed, dismissed, under_review")
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ActivityLog(BaseModel):
    """Activity tracking log entry."""
    log_id: Optional[str] = None
    action: str = Field(..., description="patient_created, note_added, match_run, search_performed, etc.")
    user: str = ""
    details: str = ""
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
