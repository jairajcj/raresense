"""
RareSense.AI — Pydantic Models for Patients & Clinical Data
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ExtractedEntity(BaseModel):
    """An NLP-extracted medical entity from clinical text."""
    entity_type: str = Field(..., description="Type: symptom, diagnosis, medication, lab_value")
    text: str = Field(..., description="Original text from clinical note")
    normalized_name: str = Field(..., description="Standardized medical term")
    hpo_code: Optional[str] = Field(None, description="HPO code e.g. HP:0000958")
    confidence: float = Field(0.0, ge=0.0, le=1.0)


class LabResult(BaseModel):
    """A laboratory test result."""
    test_name: str
    value: float
    unit: str
    reference_min: Optional[float] = None
    reference_max: Optional[float] = None
    is_abnormal: bool = False
    date: datetime


class ClinicalNote(BaseModel):
    """A clinical note (discharge summary, progress note, etc.)."""
    note_id: Optional[str] = None
    patient_id: str
    note_type: str = Field(..., description="discharge_summary, progress_note, consultation, radiology")
    specialty: str = Field("General", description="Medical specialty of the authoring physician")
    physician: str = ""
    date: datetime
    text: str = Field(..., description="Raw clinical note text")
    extracted_entities: List[ExtractedEntity] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ClinicalNoteCreate(BaseModel):
    """Schema for creating a new clinical note."""
    note_type: str
    specialty: str = "General"
    physician: str = ""
    date: datetime
    text: str

class ClinicalNoteUpdate(BaseModel):
    """Schema for updating an existing clinical note (timeline edit)."""
    note_type: Optional[str] = None
    specialty: Optional[str] = None
    physician: Optional[str] = None
    date: Optional[datetime] = None
    text: Optional[str] = None



class Patient(BaseModel):
    """A patient record."""
    patient_id: Optional[str] = None
    user_id: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str = Field(..., description="M, F, or Other")
    blood_type: Optional[str] = None
    ethnicity: Optional[str] = None
    insurance: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []
    status: str = Field("active", description="active, discharged, deceased")
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
    notes_count: int = 0
    matches_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PatientCreate(BaseModel):
    """Schema for creating a new patient."""
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str
    blood_type: Optional[str] = None
    ethnicity: Optional[str] = None
    insurance: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []
    status: str = "active"
    admission_date: Optional[datetime] = None


class PatientUpdate(BaseModel):
    """Schema for updating a patient."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    ethnicity: Optional[str] = None
    insurance: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    status: Optional[str] = None
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
