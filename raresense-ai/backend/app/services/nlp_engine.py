"""
RareSense.AI — Clinical NLP Engine
Rule-based + keyword extraction from clinical notes.
Maps extracted symptoms to HPO codes.
Simulates BioBERT/medSpaCy output for the prototype.
"""
import re
from typing import List, Dict

# Comprehensive symptom-to-HPO mapping (simulating medSpaCy + HPO ontology)
SYMPTOM_HPO_MAP = {
    # Dermatological
    "malar rash": {"hpo": "HP:0025300", "name": "Malar rash", "type": "symptom"},
    "butterfly rash": {"hpo": "HP:0025300", "name": "Malar rash", "type": "symptom"},
    "erythematous malar rash": {"hpo": "HP:0025300", "name": "Malar rash", "type": "symptom"},
    "photosensitivity": {"hpo": "HP:0000992", "name": "Photosensitivity", "type": "symptom"},
    "skin rash": {"hpo": "HP:0000988", "name": "Skin rash", "type": "symptom"},
    "purpura": {"hpo": "HP:0000979", "name": "Purpura", "type": "symptom"},
    "petechiae": {"hpo": "HP:0000967", "name": "Petechiae", "type": "symptom"},
    "alopecia": {"hpo": "HP:0001596", "name": "Alopecia", "type": "symptom"},
    "hyperpigmentation": {"hpo": "HP:0000953", "name": "Hyperpigmentation", "type": "symptom"},
    "telangiectasia": {"hpo": "HP:0001009", "name": "Telangiectasia", "type": "symptom"},
    "raynaud": {"hpo": "HP:0030880", "name": "Raynaud phenomenon", "type": "symptom"},
    
    # Hematological
    "thrombocytopenia": {"hpo": "HP:0001873", "name": "Thrombocytopenia", "type": "symptom"},
    "low platelets": {"hpo": "HP:0001873", "name": "Thrombocytopenia", "type": "symptom"},
    "anemia": {"hpo": "HP:0001903", "name": "Anemia", "type": "symptom"},
    "hemolytic anemia": {"hpo": "HP:0001878", "name": "Hemolytic anemia", "type": "symptom"},
    "leukopenia": {"hpo": "HP:0001882", "name": "Leukopenia", "type": "symptom"},
    "pancytopenia": {"hpo": "HP:0001876", "name": "Pancytopenia", "type": "symptom"},
    "lymphopenia": {"hpo": "HP:0001888", "name": "Lymphopenia", "type": "symptom"},
    "splenomegaly": {"hpo": "HP:0001744", "name": "Splenomegaly", "type": "symptom"},
    "hepatomegaly": {"hpo": "HP:0002240", "name": "Hepatomegaly", "type": "symptom"},
    
    # Renal
    "proteinuria": {"hpo": "HP:0000790", "name": "Proteinuria", "type": "symptom"},
    "hematuria": {"hpo": "HP:0000790", "name": "Hematuria", "type": "symptom"},
    "reduced renal function": {"hpo": "HP:0012622", "name": "Reduced renal function", "type": "symptom"},
    "renal failure": {"hpo": "HP:0000083", "name": "Renal insufficiency", "type": "symptom"},
    "nephritis": {"hpo": "HP:0000123", "name": "Nephritis", "type": "symptom"},
    "edema": {"hpo": "HP:0000969", "name": "Edema", "type": "symptom"},
    "peripheral edema": {"hpo": "HP:0012398", "name": "Peripheral edema", "type": "symptom"},
    
    # Musculoskeletal
    "arthralgia": {"hpo": "HP:0002829", "name": "Arthralgia", "type": "symptom"},
    "joint pain": {"hpo": "HP:0002829", "name": "Arthralgia", "type": "symptom"},
    "arthritis": {"hpo": "HP:0001369", "name": "Arthritis", "type": "symptom"},
    "myalgia": {"hpo": "HP:0003326", "name": "Myalgia", "type": "symptom"},
    "muscle weakness": {"hpo": "HP:0001324", "name": "Muscle weakness", "type": "symptom"},
    "joint swelling": {"hpo": "HP:0001386", "name": "Joint swelling", "type": "symptom"},
    "morning stiffness": {"hpo": "HP:0100550", "name": "Morning stiffness", "type": "symptom"},
    
    # Neurological
    "seizures": {"hpo": "HP:0001250", "name": "Seizures", "type": "symptom"},
    "headache": {"hpo": "HP:0002315", "name": "Headache", "type": "symptom"},
    "neuropathy": {"hpo": "HP:0009830", "name": "Peripheral neuropathy", "type": "symptom"},
    "cognitive decline": {"hpo": "HP:0100543", "name": "Cognitive decline", "type": "symptom"},
    "ataxia": {"hpo": "HP:0001251", "name": "Ataxia", "type": "symptom"},
    "tremor": {"hpo": "HP:0001337", "name": "Tremor", "type": "symptom"},
    "paresthesia": {"hpo": "HP:0003401", "name": "Paresthesia", "type": "symptom"},
    "numbness": {"hpo": "HP:0003401", "name": "Paresthesia", "type": "symptom"},
    
    # Constitutional
    "fatigue": {"hpo": "HP:0012432", "name": "Chronic fatigue", "type": "symptom"},
    "chronic fatigue": {"hpo": "HP:0012432", "name": "Chronic fatigue", "type": "symptom"},
    "persistent fatigue": {"hpo": "HP:0012432", "name": "Chronic fatigue", "type": "symptom"},
    "fever": {"hpo": "HP:0001945", "name": "Fever", "type": "symptom"},
    "weight loss": {"hpo": "HP:0001824", "name": "Weight loss", "type": "symptom"},
    "malaise": {"hpo": "HP:0033834", "name": "Malaise", "type": "symptom"},
    "night sweats": {"hpo": "HP:0030166", "name": "Night sweats", "type": "symptom"},
    
    # Cardiac
    "pericarditis": {"hpo": "HP:0001701", "name": "Pericarditis", "type": "symptom"},
    "cardiomyopathy": {"hpo": "HP:0001638", "name": "Cardiomyopathy", "type": "symptom"},
    "heart murmur": {"hpo": "HP:0030148", "name": "Heart murmur", "type": "symptom"},
    "tachycardia": {"hpo": "HP:0001649", "name": "Tachycardia", "type": "symptom"},
    "bradycardia": {"hpo": "HP:0001662", "name": "Bradycardia", "type": "symptom"},
    "chest pain": {"hpo": "HP:0100749", "name": "Chest pain", "type": "symptom"},
    "dyspnea": {"hpo": "HP:0002094", "name": "Dyspnea", "type": "symptom"},
    "shortness of breath": {"hpo": "HP:0002094", "name": "Dyspnea", "type": "symptom"},
    
    # Pulmonary
    "pleural effusion": {"hpo": "HP:0002202", "name": "Pleural effusion", "type": "symptom"},
    "pulmonary fibrosis": {"hpo": "HP:0002206", "name": "Pulmonary fibrosis", "type": "symptom"},
    "cough": {"hpo": "HP:0012735", "name": "Cough", "type": "symptom"},
    "hemoptysis": {"hpo": "HP:0002105", "name": "Hemoptysis", "type": "symptom"},
    "pulmonary hypertension": {"hpo": "HP:0002092", "name": "Pulmonary hypertension", "type": "symptom"},
    
    # Gastrointestinal
    "abdominal pain": {"hpo": "HP:0002027", "name": "Abdominal pain", "type": "symptom"},
    "nausea": {"hpo": "HP:0002018", "name": "Nausea", "type": "symptom"},
    "vomiting": {"hpo": "HP:0002013", "name": "Vomiting", "type": "symptom"},
    "diarrhea": {"hpo": "HP:0002014", "name": "Diarrhea", "type": "symptom"},
    "dysphagia": {"hpo": "HP:0002015", "name": "Dysphagia", "type": "symptom"},
    "hepatitis": {"hpo": "HP:0012115", "name": "Hepatitis", "type": "symptom"},
    "jaundice": {"hpo": "HP:0000952", "name": "Jaundice", "type": "symptom"},
    
    # Ophthalmological
    "visual impairment": {"hpo": "HP:0000505", "name": "Visual impairment", "type": "symptom"},
    "uveitis": {"hpo": "HP:0000554", "name": "Uveitis", "type": "symptom"},
    "dry eyes": {"hpo": "HP:0000407", "name": "Dry eyes", "type": "symptom"},
    "optic neuritis": {"hpo": "HP:0100653", "name": "Optic neuritis", "type": "symptom"},
    
    # Endocrine
    "hypothyroidism": {"hpo": "HP:0000821", "name": "Hypothyroidism", "type": "symptom"},
    "hyperthyroidism": {"hpo": "HP:0000820", "name": "Hyperthyroidism", "type": "symptom"},
    "diabetes": {"hpo": "HP:0000819", "name": "Diabetes mellitus", "type": "symptom"},
    "growth retardation": {"hpo": "HP:0001510", "name": "Growth delay", "type": "symptom"},
    
    # Lymphatic / Immune
    "lymphadenopathy": {"hpo": "HP:0002716", "name": "Lymphadenopathy", "type": "symptom"},
    "oral ulcers": {"hpo": "HP:0011107", "name": "Oral ulcers", "type": "symptom"},
    "mouth ulcers": {"hpo": "HP:0011107", "name": "Oral ulcers", "type": "symptom"},
    "vasculitis": {"hpo": "HP:0002633", "name": "Vasculitis", "type": "symptom"},
    "immunodeficiency": {"hpo": "HP:0002721", "name": "Immunodeficiency", "type": "symptom"},
}

# Medication patterns
MEDICATION_PATTERNS = [
    r'\b(hydrocortisone|prednisone|prednisolone|dexamethasone|methylprednisolone)\b',
    r'\b(methotrexate|azathioprine|cyclophosphamide|mycophenolate|rituximab)\b',
    r'\b(hydroxychloroquine|chloroquine|plaquenil)\b',
    r'\b(warfarin|heparin|enoxaparin|aspirin|clopidogrel)\b',
    r'\b(ibuprofen|naproxen|diclofenac|celecoxib)\b',
    r'\b(lisinopril|enalapril|ramipril|losartan|valsartan)\b',
    r'\b(metformin|insulin|glipizide|sitagliptin)\b',
    r'\b(levothyroxine|propylthiouracil|methimazole)\b',
    r'\b(omeprazole|pantoprazole|esomeprazole)\b',
    r'\b(amoxicillin|ciprofloxacin|azithromycin|doxycycline|vancomycin)\b',
    r'\b(furosemide|hydrochlorothiazide|spironolactone)\b',
    r'\b(amlodipine|metoprolol|atenolol|carvedilol)\b',
]

# Diagnosis patterns
DIAGNOSIS_PATTERNS = {
    "lupus": "Systemic Lupus Erythematosus",
    "sle": "Systemic Lupus Erythematosus",
    "rheumatoid arthritis": "Rheumatoid Arthritis",
    "scleroderma": "Systemic Sclerosis",
    "systemic sclerosis": "Systemic Sclerosis",
    "vasculitis": "Vasculitis",
    "marfan": "Marfan Syndrome",
    "ehlers-danlos": "Ehlers-Danlos Syndrome",
    "gaucher": "Gaucher Disease",
    "fabry": "Fabry Disease",
    "pompe": "Pompe Disease",
    "wilson disease": "Wilson Disease",
    "huntington": "Huntington Disease",
    "cystic fibrosis": "Cystic Fibrosis",
    "sickle cell": "Sickle Cell Disease",
    "thalassemia": "Thalassemia",
    "hemophilia": "Hemophilia",
    "myasthenia gravis": "Myasthenia Gravis",
    "multiple sclerosis": "Multiple Sclerosis",
    "amyloidosis": "Amyloidosis",
    "sarcoidosis": "Sarcoidosis",
    "dermatomyositis": "Dermatomyositis",
    "polymyositis": "Polymyositis",
    "antiphospholipid": "Antiphospholipid Syndrome",
    "sjögren": "Sjögren Syndrome",
    "sjogren": "Sjögren Syndrome",
    "behçet": "Behçet Disease",
    "behcet": "Behçet Disease",
    "mixed connective tissue": "Mixed Connective Tissue Disease",
    "pheochromocytoma": "Pheochromocytoma",
    "addison": "Addison Disease",
    "cushing": "Cushing Syndrome",
}


def extract_entities(clinical_text: str) -> List[Dict]:
    """
    Extract medical entities from clinical note text.
    Simulates BioBERT + medSpaCy NER pipeline output.
    
    Returns list of extracted entities with HPO codes.
    """
    entities = []
    text_lower = clinical_text.lower()
    seen_hpo = set()
    
    # Extract symptoms
    for term, info in SYMPTOM_HPO_MAP.items():
        if term in text_lower and info["hpo"] not in seen_hpo:
            # Find the actual text match for context
            idx = text_lower.find(term)
            # Get surrounding context (up to 40 chars before and after)
            start = max(0, idx - 40)
            end = min(len(clinical_text), idx + len(term) + 40)
            context = clinical_text[start:end].strip()
            
            entities.append({
                "entity_type": info["type"],
                "text": context,
                "normalized_name": info["name"],
                "hpo_code": info["hpo"],
                "confidence": 0.85 + (0.15 * (len(term) / 20))  # Longer terms = higher confidence
            })
            seen_hpo.add(info["hpo"])
    
    # Extract medications
    for pattern in MEDICATION_PATTERNS:
        matches = re.findall(pattern, text_lower)
        for med in matches:
            entities.append({
                "entity_type": "medication",
                "text": med,
                "normalized_name": med.capitalize(),
                "hpo_code": None,
                "confidence": 0.95
            })
    
    # Extract diagnoses
    for term, diagnosis in DIAGNOSIS_PATTERNS.items():
        if term in text_lower:
            entities.append({
                "entity_type": "diagnosis",
                "text": term,
                "normalized_name": diagnosis,
                "hpo_code": None,
                "confidence": 0.90
            })
    
    # Extract lab values using regex
    lab_patterns = [
        (r'platelet\s*(?:count)?\s*(?:of\s*)?(\d+[\.,]?\d*)\s*(?:/uL|×10\^3|k)', "Platelet Count", "/uL", 150000, 400000),
        (r'hemoglobin\s*(?:of\s*)?(\d+\.?\d*)\s*(?:g/dL|g/dl)', "Hemoglobin", "g/dL", 12.0, 17.5),
        (r'(?:wbc|white blood cell)\s*(?:count)?\s*(?:of\s*)?(\d+\.?\d*)\s*(?:k|×10\^3|/uL)', "WBC Count", "×10³/μL", 4.5, 11.0),
        (r'creatinine\s*(?:of\s*)?(\d+\.?\d*)\s*(?:mg/dL|mg/dl)', "Creatinine", "mg/dL", 0.6, 1.2),
        (r'(?:eGFR|gfr)\s*(?:of\s*)?(\d+\.?\d*)', "eGFR", "mL/min", 90, 120),
        (r'(?:ESR|sed rate)\s*(?:of\s*)?(\d+\.?\d*)\s*(?:mm/hr)?', "ESR", "mm/hr", 0, 20),
        (r'(?:CRP|c-reactive protein)\s*(?:of\s*)?(\d+\.?\d*)\s*(?:mg/[Ll])?', "CRP", "mg/L", 0, 10),
        (r'ANA\s*(?:titer)?\s*(?:of\s*)?(?:1:)?(\d+)', "ANA Titer", "titer", 0, 40),
    ]
    
    for pattern, name, unit, ref_min, ref_max in lab_patterns:
        match = re.search(pattern, clinical_text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1).replace(',', ''))
                is_abnormal = value < ref_min or value > ref_max
                entities.append({
                    "entity_type": "lab_value",
                    "text": match.group(0),
                    "normalized_name": name,
                    "hpo_code": None,
                    "confidence": 0.92,
                    "lab_data": {
                        "value": value,
                        "unit": unit,
                        "reference_min": ref_min,
                        "reference_max": ref_max,
                        "is_abnormal": is_abnormal
                    }
                })
            except ValueError:
                pass
    
    return entities


def get_patient_phenotype(entities_list: List[List[Dict]]) -> List[str]:
    """
    Given a list of entity lists (from multiple notes), extract unique HPO codes
    representing the patient's phenotype profile.
    """
    hpo_codes = set()
    for entities in entities_list:
        for entity in entities:
            if entity.get("hpo_code"):
                hpo_codes.add(entity["hpo_code"])
    return list(hpo_codes)
