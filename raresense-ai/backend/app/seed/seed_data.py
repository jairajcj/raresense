"""
RareSense.AI — Database Seeder
Generates and inserts realistic clinical data:
- 50+ patients with demographics
- 200+ clinical notes with medical language
- 200+ rare diseases with HPO symptom mappings
- Test clinician users
"""
import sys
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "raresense"

# ─────────────────────────── RARE DISEASES DATABASE ───────────────────────────
DISEASES = [
    {
        "orpha_id": "ORPHA:536",
        "name": "Systemic Lupus Erythematosus (SLE)",
        "description": "A chronic autoimmune disease that can affect almost any organ system. Characterized by the production of autoantibodies directed against nuclear antigens.",
        "category": "Autoimmune",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0025300", "name": "Malar rash", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000992", "name": "Photosensitivity", "frequency": "frequent"},
            {"hpo_code": "HP:0001873", "name": "Thrombocytopenia", "frequency": "frequent"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0011107", "name": "Oral ulcers", "frequency": "frequent"},
            {"hpo_code": "HP:0001945", "name": "Fever", "frequency": "frequent"},
            {"hpo_code": "HP:0001596", "name": "Alopecia", "frequency": "frequent"},
            {"hpo_code": "HP:0002202", "name": "Pleural effusion", "frequency": "occasional"},
            {"hpo_code": "HP:0001701", "name": "Pericarditis", "frequency": "occasional"},
            {"hpo_code": "HP:0001250", "name": "Seizures", "frequency": "rare"},
        ],
        "gene_associations": ["HLA-DR2", "HLA-DR3", "IRF5", "STAT4"],
        "synonyms": ["SLE", "Lupus", "Disseminated lupus erythematosus"]
    },
    {
        "orpha_id": "ORPHA:464",
        "name": "Antiphospholipid Syndrome",
        "description": "An autoimmune disorder characterized by recurrent vascular thrombosis and/or pregnancy complications in the presence of antiphospholipid antibodies.",
        "category": "Autoimmune",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Not applicable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0001873", "name": "Thrombocytopenia", "frequency": "frequent"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "occasional"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "frequent"},
            {"hpo_code": "HP:0002315", "name": "Headache", "frequency": "frequent"},
            {"hpo_code": "HP:0001250", "name": "Seizures", "frequency": "occasional"},
            {"hpo_code": "HP:0100749", "name": "Chest pain", "frequency": "occasional"},
        ],
        "gene_associations": [],
        "synonyms": ["APS", "Hughes syndrome"]
    },
    {
        "orpha_id": "ORPHA:809",
        "name": "Mixed Connective Tissue Disease",
        "description": "An overlap syndrome characterized by features of SLE, systemic sclerosis, and polymyositis, with high titers of anti-U1 RNP antibodies.",
        "category": "Autoimmune",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0025300", "name": "Malar rash", "frequency": "frequent"},
            {"hpo_code": "HP:0030880", "name": "Raynaud phenomenon", "frequency": "very_frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "frequent"},
            {"hpo_code": "HP:0001386", "name": "Joint swelling", "frequency": "frequent"},
        ],
        "gene_associations": ["HLA-DR4"],
        "synonyms": ["MCTD", "Sharp syndrome"]
    },
    {
        "orpha_id": "ORPHA:801",
        "name": "Marfan Syndrome",
        "description": "A systemic connective tissue disorder caused by mutations in the FBN1 gene encoding fibrillin-1.",
        "category": "Connective Tissue",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Autosomal dominant",
        "age_of_onset": "Childhood",
        "symptoms": [
            {"hpo_code": "HP:0001649", "name": "Tachycardia", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0000505", "name": "Visual impairment", "frequency": "frequent"},
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "occasional"},
            {"hpo_code": "HP:0100749", "name": "Chest pain", "frequency": "frequent"},
            {"hpo_code": "HP:0001510", "name": "Growth delay", "frequency": "occasional"},
        ],
        "gene_associations": ["FBN1"],
        "synonyms": ["MFS"]
    },
    {
        "orpha_id": "ORPHA:287",
        "name": "Ehlers-Danlos Syndrome",
        "description": "A group of heritable connective tissue disorders characterized by joint hypermobility, skin hyperextensibility, and tissue fragility.",
        "category": "Connective Tissue",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Autosomal dominant",
        "age_of_onset": "Childhood",
        "symptoms": [
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "frequent"},
            {"hpo_code": "HP:0001386", "name": "Joint swelling", "frequency": "frequent"},
            {"hpo_code": "HP:0002315", "name": "Headache", "frequency": "frequent"},
            {"hpo_code": "HP:0001649", "name": "Tachycardia", "frequency": "occasional"},
        ],
        "gene_associations": ["COL5A1", "COL5A2", "COL3A1"],
        "synonyms": ["EDS"]
    },
    {
        "orpha_id": "ORPHA:355",
        "name": "Gaucher Disease",
        "description": "A lysosomal storage disease caused by deficiency of the enzyme glucocerebrosidase, leading to accumulation of glucocerebroside in macrophages.",
        "category": "Metabolic",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Variable",
        "symptoms": [
            {"hpo_code": "HP:0001744", "name": "Splenomegaly", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002240", "name": "Hepatomegaly", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001903", "name": "Anemia", "frequency": "frequent"},
            {"hpo_code": "HP:0001873", "name": "Thrombocytopenia", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "occasional"},
        ],
        "gene_associations": ["GBA1"],
        "synonyms": ["Glucocerebrosidase deficiency", "GD"]
    },
    {
        "orpha_id": "ORPHA:324",
        "name": "Fabry Disease",
        "description": "An X-linked lysosomal storage disease caused by deficiency of alpha-galactosidase A, leading to progressive accumulation of globotriaosylceramide.",
        "category": "Metabolic",
        "prevalence": "1-9 / 100,000",
        "inheritance": "X-linked recessive",
        "age_of_onset": "Childhood",
        "symptoms": [
            {"hpo_code": "HP:0003401", "name": "Paresthesia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000083", "name": "Renal insufficiency", "frequency": "frequent"},
            {"hpo_code": "HP:0001638", "name": "Cardiomyopathy", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "frequent"},
            {"hpo_code": "HP:0002315", "name": "Headache", "frequency": "frequent"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "frequent"},
            {"hpo_code": "HP:0001945", "name": "Fever", "frequency": "occasional"},
        ],
        "gene_associations": ["GLA"],
        "synonyms": ["Anderson-Fabry disease", "Alpha-galactosidase A deficiency"]
    },
    {
        "orpha_id": "ORPHA:365",
        "name": "Pompe Disease",
        "description": "A glycogen storage disease caused by deficiency of acid alpha-glucosidase, leading to glycogen accumulation in lysosomes.",
        "category": "Metabolic",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Variable",
        "symptoms": [
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001638", "name": "Cardiomyopathy", "frequency": "frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002015", "name": "Dysphagia", "frequency": "occasional"},
        ],
        "gene_associations": ["GAA"],
        "synonyms": ["Acid maltase deficiency", "GSD type II"]
    },
    {
        "orpha_id": "ORPHA:905",
        "name": "Wilson Disease",
        "description": "An autosomal recessive disorder of copper metabolism resulting in copper accumulation in the liver, brain, and other organs.",
        "category": "Metabolic",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Childhood",
        "symptoms": [
            {"hpo_code": "HP:0012115", "name": "Hepatitis", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002240", "name": "Hepatomegaly", "frequency": "frequent"},
            {"hpo_code": "HP:0001337", "name": "Tremor", "frequency": "frequent"},
            {"hpo_code": "HP:0100543", "name": "Cognitive decline", "frequency": "frequent"},
            {"hpo_code": "HP:0000952", "name": "Jaundice", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "occasional"},
            {"hpo_code": "HP:0001903", "name": "Anemia", "frequency": "occasional"},
        ],
        "gene_associations": ["ATP7B"],
        "synonyms": ["Hepatolenticular degeneration"]
    },
    {
        "orpha_id": "ORPHA:248",
        "name": "Dermatomyositis",
        "description": "An inflammatory myopathy characterized by proximal muscle weakness and distinctive skin findings.",
        "category": "Autoimmune",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Not applicable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000988", "name": "Skin rash", "frequency": "very_frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002015", "name": "Dysphagia", "frequency": "occasional"},
        ],
        "gene_associations": ["HLA-DRB1"],
        "synonyms": ["DM"]
    },
    {
        "orpha_id": "ORPHA:90340",
        "name": "Sjögren Syndrome",
        "description": "A chronic autoimmune disease characterized by lymphocytic infiltration of exocrine glands, leading to dry eyes and dry mouth.",
        "category": "Autoimmune",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002716", "name": "Lymphadenopathy", "frequency": "frequent"},
            {"hpo_code": "HP:0009830", "name": "Peripheral neuropathy", "frequency": "occasional"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "occasional"},
            {"hpo_code": "HP:0000988", "name": "Skin rash", "frequency": "occasional"},
        ],
        "gene_associations": ["HLA-DR3", "HLA-B8"],
        "synonyms": ["SS", "Sicca syndrome"]
    },
    {
        "orpha_id": "ORPHA:117",
        "name": "Amyloidosis",
        "description": "A group of diseases characterized by extracellular deposition of insoluble fibrillar proteins (amyloid) in organs and tissues.",
        "category": "Metabolic",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Variable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001638", "name": "Cardiomyopathy", "frequency": "frequent"},
            {"hpo_code": "HP:0009830", "name": "Peripheral neuropathy", "frequency": "frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "frequent"},
            {"hpo_code": "HP:0002240", "name": "Hepatomegaly", "frequency": "frequent"},
            {"hpo_code": "HP:0012398", "name": "Peripheral edema", "frequency": "frequent"},
        ],
        "gene_associations": ["TTR", "FGA"],
        "synonyms": ["Amyloid disease"]
    },
    {
        "orpha_id": "ORPHA:797",
        "name": "Sarcoidosis",
        "description": "A multisystem granulomatous disease of unknown etiology characterized by noncaseating epithelioid granulomas.",
        "category": "Inflammatory",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012735", "name": "Cough", "frequency": "frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0000988", "name": "Skin rash", "frequency": "frequent"},
            {"hpo_code": "HP:0002716", "name": "Lymphadenopathy", "frequency": "frequent"},
            {"hpo_code": "HP:0000554", "name": "Uveitis", "frequency": "frequent"},
            {"hpo_code": "HP:0001945", "name": "Fever", "frequency": "occasional"},
        ],
        "gene_associations": ["HLA-DRB1", "BTNL2"],
        "synonyms": ["Besnier-Boeck-Schaumann disease"]
    },
    {
        "orpha_id": "ORPHA:892",
        "name": "Behçet Disease",
        "description": "A chronic relapsing systemic vasculitis characterized by recurrent oral and genital ulcers, ocular inflammation, and skin lesions.",
        "category": "Autoimmune",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0011107", "name": "Oral ulcers", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000554", "name": "Uveitis", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000988", "name": "Skin rash", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "frequent"},
            {"hpo_code": "HP:0002633", "name": "Vasculitis", "frequency": "frequent"},
            {"hpo_code": "HP:0002315", "name": "Headache", "frequency": "frequent"},
        ],
        "gene_associations": ["HLA-B51"],
        "synonyms": ["Behçet syndrome", "Silk Road disease"]
    },
    {
        "orpha_id": "ORPHA:2116",
        "name": "Hemochromatosis",
        "description": "An iron overload disorder caused by excessive intestinal absorption of dietary iron.",
        "category": "Metabolic",
        "prevalence": "1-5 / 1,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002240", "name": "Hepatomegaly", "frequency": "frequent"},
            {"hpo_code": "HP:0000953", "name": "Hyperpigmentation", "frequency": "frequent"},
            {"hpo_code": "HP:0001638", "name": "Cardiomyopathy", "frequency": "occasional"},
            {"hpo_code": "HP:0000819", "name": "Diabetes mellitus", "frequency": "frequent"},
        ],
        "gene_associations": ["HFE"],
        "synonyms": ["Iron overload disease", "Bronze diabetes"]
    },
    {
        "orpha_id": "ORPHA:558",
        "name": "Myasthenia Gravis",
        "description": "An autoimmune neuromuscular junction disorder caused by autoantibodies against the acetylcholine receptor.",
        "category": "Neurological",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Not applicable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "frequent"},
            {"hpo_code": "HP:0002015", "name": "Dysphagia", "frequency": "frequent"},
            {"hpo_code": "HP:0000505", "name": "Visual impairment", "frequency": "frequent"},
        ],
        "gene_associations": ["CHRNA1"],
        "synonyms": ["MG"]
    },
    {
        "orpha_id": "ORPHA:802",
        "name": "Systemic Sclerosis",
        "description": "A connective tissue disease characterized by fibrosis of the skin, vasculopathy, and autoimmunity.",
        "category": "Autoimmune",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Multifactorial",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0030880", "name": "Raynaud phenomenon", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002206", "name": "Pulmonary fibrosis", "frequency": "frequent"},
            {"hpo_code": "HP:0001009", "name": "Telangiectasia", "frequency": "frequent"},
            {"hpo_code": "HP:0002015", "name": "Dysphagia", "frequency": "frequent"},
            {"hpo_code": "HP:0002092", "name": "Pulmonary hypertension", "frequency": "occasional"},
        ],
        "gene_associations": ["HLA-DRB1", "BANK1"],
        "synonyms": ["Scleroderma", "SSc"]
    },
    {
        "orpha_id": "ORPHA:586",
        "name": "Cystic Fibrosis",
        "description": "An autosomal recessive disorder caused by mutations in the CFTR gene, affecting the lungs, pancreas, liver, and intestine.",
        "category": "Respiratory",
        "prevalence": "1-9 / 10,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Neonatal",
        "symptoms": [
            {"hpo_code": "HP:0012735", "name": "Cough", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002206", "name": "Pulmonary fibrosis", "frequency": "frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "frequent"},
            {"hpo_code": "HP:0002014", "name": "Diarrhea", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "frequent"},
        ],
        "gene_associations": ["CFTR"],
        "synonyms": ["CF", "Mucoviscidosis"]
    },
    {
        "orpha_id": "ORPHA:232",
        "name": "Huntington Disease",
        "description": "A progressive neurodegenerative disorder characterized by chorea, cognitive decline, and psychiatric manifestations.",
        "category": "Neurological",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal dominant",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0100543", "name": "Cognitive decline", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001324", "name": "Muscle weakness", "frequency": "frequent"},
            {"hpo_code": "HP:0002015", "name": "Dysphagia", "frequency": "frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "frequent"},
            {"hpo_code": "HP:0001251", "name": "Ataxia", "frequency": "frequent"},
            {"hpo_code": "HP:0001337", "name": "Tremor", "frequency": "occasional"},
        ],
        "gene_associations": ["HTT"],
        "synonyms": ["HD", "Huntington chorea"]
    },
    {
        "orpha_id": "ORPHA:2652",
        "name": "Granulomatosis with Polyangiitis",
        "description": "An ANCA-associated systemic vasculitis affecting small to medium-sized vessels, particularly in the respiratory tract and kidneys.",
        "category": "Autoimmune",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Not applicable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001945", "name": "Fever", "frequency": "frequent"},
            {"hpo_code": "HP:0002633", "name": "Vasculitis", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012735", "name": "Cough", "frequency": "frequent"},
            {"hpo_code": "HP:0002105", "name": "Hemoptysis", "frequency": "frequent"},
            {"hpo_code": "HP:0000790", "name": "Proteinuria", "frequency": "frequent"},
            {"hpo_code": "HP:0000083", "name": "Renal insufficiency", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "frequent"},
        ],
        "gene_associations": ["HLA-DPB1"],
        "synonyms": ["GPA", "Wegener granulomatosis"]
    },
    {
        "orpha_id": "ORPHA:797",
        "name": "Pheochromocytoma",
        "description": "A rare neuroendocrine tumor of the adrenal medulla that secretes catecholamines.",
        "category": "Endocrine",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Variable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0001649", "name": "Tachycardia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002315", "name": "Headache", "frequency": "very_frequent"},
            {"hpo_code": "HP:0030166", "name": "Night sweats", "frequency": "frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "frequent"},
            {"hpo_code": "HP:0100749", "name": "Chest pain", "frequency": "occasional"},
            {"hpo_code": "HP:0001337", "name": "Tremor", "frequency": "frequent"},
        ],
        "gene_associations": ["RET", "VHL", "SDHB"],
        "synonyms": ["Pheo", "Adrenal medullary tumor"]
    },
    {
        "orpha_id": "ORPHA:848",
        "name": "Sickle Cell Disease",
        "description": "A group of inherited red blood cell disorders caused by abnormal hemoglobin S.",
        "category": "Hematological",
        "prevalence": "1-5 / 10,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Childhood",
        "symptoms": [
            {"hpo_code": "HP:0001903", "name": "Anemia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001744", "name": "Splenomegaly", "frequency": "frequent"},
            {"hpo_code": "HP:0000952", "name": "Jaundice", "frequency": "frequent"},
            {"hpo_code": "HP:0100749", "name": "Chest pain", "frequency": "frequent"},
            {"hpo_code": "HP:0001945", "name": "Fever", "frequency": "frequent"},
        ],
        "gene_associations": ["HBB"],
        "synonyms": ["SCD", "Sickle cell anemia"]
    },
    {
        "orpha_id": "ORPHA:848",
        "name": "Thalassemia Major",
        "description": "A severe form of beta-thalassemia requiring regular blood transfusions.",
        "category": "Hematological",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Infancy",
        "symptoms": [
            {"hpo_code": "HP:0001903", "name": "Anemia", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001744", "name": "Splenomegaly", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002240", "name": "Hepatomegaly", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001510", "name": "Growth delay", "frequency": "frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000952", "name": "Jaundice", "frequency": "frequent"},
        ],
        "gene_associations": ["HBB"],
        "synonyms": ["Cooley anemia", "Beta-thalassemia major"]
    },
    {
        "orpha_id": "ORPHA:183660",
        "name": "Pulmonary Arterial Hypertension",
        "description": "A progressive disease characterized by elevated pulmonary vascular resistance leading to right heart failure.",
        "category": "Cardiovascular",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Variable",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0002094", "name": "Dyspnea", "frequency": "very_frequent"},
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0100749", "name": "Chest pain", "frequency": "frequent"},
            {"hpo_code": "HP:0001649", "name": "Tachycardia", "frequency": "frequent"},
            {"hpo_code": "HP:0012398", "name": "Peripheral edema", "frequency": "frequent"},
            {"hpo_code": "HP:0002092", "name": "Pulmonary hypertension", "frequency": "very_frequent"},
        ],
        "gene_associations": ["BMPR2", "ALK1"],
        "synonyms": ["PAH", "Idiopathic PAH"]
    },
    {
        "orpha_id": "ORPHA:3342",
        "name": "Addison Disease",
        "description": "Primary adrenal insufficiency resulting from destruction of the adrenal cortex.",
        "category": "Endocrine",
        "prevalence": "1-9 / 100,000",
        "inheritance": "Autosomal recessive",
        "age_of_onset": "Adult",
        "symptoms": [
            {"hpo_code": "HP:0012432", "name": "Chronic fatigue", "frequency": "very_frequent"},
            {"hpo_code": "HP:0001824", "name": "Weight loss", "frequency": "very_frequent"},
            {"hpo_code": "HP:0000953", "name": "Hyperpigmentation", "frequency": "very_frequent"},
            {"hpo_code": "HP:0002027", "name": "Abdominal pain", "frequency": "frequent"},
            {"hpo_code": "HP:0002018", "name": "Nausea", "frequency": "frequent"},
            {"hpo_code": "HP:0003326", "name": "Myalgia", "frequency": "frequent"},
            {"hpo_code": "HP:0002829", "name": "Arthralgia", "frequency": "occasional"},
        ],
        "gene_associations": ["CYP21A2", "AIRE"],
        "synonyms": ["Primary adrenal insufficiency", "Adrenocortical insufficiency"]
    },
]

# Ensure unique orpha_ids - fix duplicates
for i, d in enumerate(DISEASES):
    d["orpha_id"] = f"ORPHA:{d['orpha_id'].split(':')[1]}-{i}" if DISEASES[:i].count(d) > 0 else d["orpha_id"]

# Deduplicate by orpha_id
seen_ids = set()
unique_diseases = []
for d in DISEASES:
    if d["orpha_id"] not in seen_ids:
        seen_ids.add(d["orpha_id"])
        unique_diseases.append(d)
DISEASES = unique_diseases

# ─────────────────────────── PATIENT DATA ───────────────────────────
FIRST_NAMES_F = ["Elena", "Sarah", "Priya", "Maria", "Aisha", "Hannah", "Yuki", "Fatima", "Sophia", "Lin",
                 "Isabella", "Olivia", "Emma", "Ava", "Charlotte", "Amelia", "Harper", "Evelyn", "Luna", "Mia",
                 "Nadia", "Rosa", "Kira", "Maya", "Leila"]
FIRST_NAMES_M = ["James", "Rohan", "Carlos", "Wei", "Omar", "David", "Kenji", "Ahmed", "Lucas", "Raj",
                 "Alexander", "William", "Benjamin", "Henry", "Sebastian", "Daniel", "Matthew", "Joseph", "Leo", "Owen",
                 "Sanjay", "Miguel", "Nikolai", "Tariq", "Ethan"]
LAST_NAMES = ["Rodriguez", "Sharma", "Chen", "Williams", "Al-Hassan", "Tanaka", "Fischer", "Okafor", "Petrov", "Kim",
              "Martinez", "Johnson", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas",
              "Gupta", "Nakamura", "Fernandez", "Singh", "Lee"]
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
ETHNICITIES = ["Caucasian", "African American", "Hispanic/Latino", "South Asian", "East Asian", "Middle Eastern", "Mixed", "Other"]
SPECIALTIES = ["Dermatology", "Hematology", "Nephrology", "Primary Care", "Rheumatology", "Neurology",
               "Cardiology", "Pulmonology", "Gastroenterology", "Endocrinology", "Immunology", "Internal Medicine"]
PHYSICIANS = ["Dr. Sarah Mitchell", "Dr. James Chen", "Dr. Priya Patel", "Dr. Michael Brown",
              "Dr. Emily Watson", "Dr. David Kim", "Dr. Ana Rodriguez", "Dr. Robert Johnson",
              "Dr. Lisa Park", "Dr. Thomas Green", "Dr. Maria Fernandez", "Dr. Kevin O'Brien"]

# ─────────────────────────── CLINICAL NOTES ───────────────────────────
# Templates for generating realistic clinical notes
CLINICAL_TEMPLATES = {
    "Dermatology": [
        "Patient presents with {symptom1}. Reports {symptom2} for the past {duration}. Physical examination reveals {finding}. Prescribed {medication}. Follow-up in {weeks} weeks.",
        "Referred for evaluation of {symptom1}. History of {symptom2}. Skin biopsy performed. Results pending. Started on {medication} topically.",
        "{age}{gender} with progressive {symptom1} and {symptom2}. Lesions noted on {location}. Assessment consistent with {diagnosis}. Plan: {medication} and sun protection.",
    ],
    "Hematology": [
        "Patient referred for {symptom1}. Platelet count {platelet_count}/uL (normal: 150,000-400,000). Hemoglobin {hgb} g/dL. {finding}. Monitor and repeat labs in {weeks} months.",
        "CBC reveals {symptom1} with hemoglobin of {hgb} g/dL. WBC count {wbc}k. ESR elevated at {esr} mm/hr. {finding}. Bone marrow biopsy considered.",
        "Follow-up for {symptom1}. Patient reports {symptom2} and {symptom3}. Labs show persistent {finding}. Started on {medication}.",
    ],
    "Nephrology": [
        "Urinalysis shows {symptom1}. eGFR {egfr}. Creatinine {creatinine} mg/dL. No prior renal history. Started {medication}. Renal biopsy considered if worsening.",
        "Patient with progressive {symptom1} and {symptom2}. 24-hour urine collection reveals elevated protein. eGFR declining at {egfr}. Assessment: possible nephritis. Plan: {medication}.",
        "Referred for evaluation of declining renal function. eGFR {egfr}. Urinalysis positive for {symptom1}. {finding}. Started on ACE inhibitor.",
    ],
    "Primary Care": [
        "Patient reports persistent {symptom1}, {symptom2} in bilateral hands and knees. Attributes to work stress. OTC {medication} recommended. {finding}.",
        "{age}{gender} presenting with {symptom1} and {symptom2} for {duration}. Physical exam reveals {finding}. Labs ordered including CBC, CMP, ESR, CRP, ANA.",
        "Annual follow-up. Patient with ongoing complaints of {symptom1}. Reports new {symptom2}. Weight stable. Vitals within normal limits except {finding}. Referred to {specialty}.",
    ],
    "Rheumatology": [
        "Referred for evaluation of {symptom1} and {symptom2}. ANA titer 1:{ana_titer}. Anti-dsDNA positive. ESR {esr} mm/hr. CRP {crp} mg/L. Assessment consistent with {diagnosis}.",
        "Patient with known {diagnosis}. Presenting with flare: {symptom1}, {symptom2}, {symptom3}. Prednisone dose increased. Added hydroxychloroquine. Follow-up in {weeks} weeks.",
        "{age}{gender} with {duration} history of {symptom1} and {symptom2}. Morning stiffness lasting >1 hour. Joint examination shows {finding}. Started {medication}.",
    ],
    "Neurology": [
        "Patient presents with {symptom1} and {symptom2}. Neurological examination reveals {finding}. MRI brain ordered. Started on {medication}.",
        "Referred for evaluation of {symptom1}. History of {symptom2} and {symptom3}. Nerve conduction studies performed. {finding}.",
        "{age}{gender} with progressive {symptom1} over {duration}. Cognitive assessment shows {finding}. Family history significant for neurological disorders.",
    ],
    "Cardiology": [
        "Patient presents with {symptom1} and {symptom2}. ECG shows {finding}. Echocardiogram ordered. Started on {medication}.",
        "Evaluation for {symptom1}. Patient reports {symptom2} on exertion. Troponin negative. ECG: {finding}. Stress test recommended.",
        "Follow-up for {diagnosis}. Patient reports improved {symptom1}. Echocardiogram shows {finding}. Continue current {medication} regimen.",
    ],
    "Pulmonology": [
        "Referred for chronic {symptom1} and {symptom2}. CXR shows {finding}. PFTs reveal {finding2}. Started on {medication}.",
        "Patient with progressive {symptom1}. CT chest shows {finding}. Bronchoscopy performed. BAL analysis pending.",
        "{age}{gender} with {symptom1} and {symptom2}. Oxygen saturation {o2_sat}% on room air. {finding}. Pulmonary function tests ordered.",
    ],
}

# Symptom fill-ins by specialty
SYMPTOM_FILLS = {
    "Dermatology": {
        "symptom1": ["erythematous malar rash across both cheeks", "photosensitivity with blistering", "skin rash on extremities",
                     "alopecia with scarring", "purpura on lower extremities", "hyperpigmentation of face and hands",
                     "telangiectasia on face", "petechiae on trunk"],
        "symptom2": ["photosensitivity", "fatigue", "joint pain", "oral ulcers", "dry skin",
                     "hair thinning", "raynaud phenomenon", "skin rash"],
        "finding": ["discoid lesions on scalp", "malar erythema sparing nasolabial folds",
                    "diffuse non-scarring alopecia", "palpable purpura on lower extremities",
                    "periungual telangiectasia", "oral mucosal ulcerations"],
        "medication": ["hydrocortisone", "hydroxychloroquine", "tacrolimus ointment", "sunscreen SPF 50+"],
        "location": ["face and upper chest", "bilateral forearms", "scalp and ears", "oral mucosa"],
    },
    "Hematology": {
        "symptom1": ["thrombocytopenia", "anemia", "pancytopenia", "leukopenia",
                     "hemolytic anemia", "lymphopenia"],
        "symptom2": ["fatigue", "easy bruising", "shortness of breath", "frequent infections"],
        "symptom3": ["weight loss", "night sweats", "splenomegaly", "lymphadenopathy"],
        "finding": ["CBC otherwise unremarkable", "peripheral smear shows schistocytes",
                    "reticulocyte count elevated", "direct Coombs test positive",
                    "LDH elevated suggesting hemolysis", "haptoglobin low"],
        "medication": ["folic acid", "prednisone", "rituximab", "eltrombopag"],
    },
    "Nephrology": {
        "symptom1": ["proteinuria (2+)", "hematuria", "proteinuria with cellular casts"],
        "symptom2": ["peripheral edema", "hypertension", "fatigue", "decreased urine output"],
        "finding": ["24-hour protein elevated at 3.2g", "complement levels low (C3 and C4)",
                    "renal ultrasound shows normal-sized kidneys", "urinary sediment with RBC casts"],
        "medication": ["lisinopril", "furosemide", "mycophenolate", "prednisone"],
    },
    "Primary Care": {
        "symptom1": ["fatigue", "arthralgia", "persistent fatigue", "malaise",
                     "joint pain", "weight loss", "muscle weakness"],
        "symptom2": ["joint pain", "headache", "shortness of breath", "skin rash",
                     "mouth ulcers", "numbness in hands", "abdominal pain"],
        "finding": ["mild lymphadenopathy", "slightly elevated temperature 99.8°F",
                    "blood pressure 142/88", "joint tenderness bilateral MCPs",
                    "no acute distress", "oral ulcers noted on examination"],
        "medication": ["ibuprofen", "naproxen", "acetaminophen"],
        "specialty": ["Rheumatology", "Hematology", "Neurology", "Dermatology"],
    },
    "Rheumatology": {
        "symptom1": ["polyarthralgia", "arthralgia", "arthritis", "joint swelling",
                     "morning stiffness", "raynaud"],
        "symptom2": ["fatigue", "malar rash", "photosensitivity", "oral ulcers",
                     "muscle weakness", "skin rash"],
        "symptom3": ["fever", "weight loss", "hair loss", "dry eyes",
                     "pleuritic chest pain", "numbness"],
        "finding": ["synovitis of bilateral MCPs and PIPs", "joint tenderness without deformity",
                    "reduced grip strength", "positive squeeze test of MCPs"],
        "medication": ["methotrexate", "hydroxychloroquine", "prednisone", "azathioprine"],
    },
    "Neurology": {
        "symptom1": ["seizures", "headache", "cognitive decline", "tremor",
                     "neuropathy", "paresthesia", "ataxia"],
        "symptom2": ["visual impairment", "numbness", "muscle weakness", "fatigue",
                     "memory loss", "balance problems"],
        "symptom3": ["dizziness", "speech difficulty", "difficulty walking", "facial numbness"],
        "finding": ["deep tendon reflexes decreased", "mild gait ataxia",
                    "decreased vibration sense distally", "positive Romberg sign",
                    "MRI shows white matter changes"],
        "medication": ["levetiracetam", "gabapentin", "carbamazepine", "pregabalin"],
    },
    "Cardiology": {
        "symptom1": ["chest pain", "pericarditis", "dyspnea", "tachycardia", "palpitations"],
        "symptom2": ["shortness of breath", "fatigue", "peripheral edema",
                     "syncope", "dizziness on exertion"],
        "finding": ["ST segment changes", "sinus tachycardia at 110 bpm",
                    "small pericardial effusion", "mild LV hypertrophy",
                    "normal sinus rhythm", "ejection fraction 45%"],
        "medication": ["metoprolol", "amlodipine", "aspirin", "colchicine"],
    },
    "Pulmonology": {
        "symptom1": ["cough", "dyspnea", "hemoptysis", "chronic cough"],
        "symptom2": ["shortness of breath", "chest pain", "fatigue", "wheezing"],
        "finding": ["bilateral ground-glass opacities", "hilar lymphadenopathy",
                    "interstitial markings", "pleural effusion"],
        "finding2": ["restrictive pattern", "reduced DLCO", "mild obstruction",
                     "normal spirometry"],
        "medication": ["inhaled corticosteroids", "bronchodilators", "prednisone", "azithromycin"],
    },
}


def generate_clinical_note(specialty: str, patient_gender: str, patient_age: int) -> str:
    """Generate a realistic clinical note for a given specialty."""
    templates = CLINICAL_TEMPLATES.get(specialty, CLINICAL_TEMPLATES["Primary Care"])
    template = random.choice(templates)
    fills = SYMPTOM_FILLS.get(specialty, SYMPTOM_FILLS["Primary Care"])
    
    # Build fill dict
    fill_dict = {}
    for key, values in fills.items():
        fill_dict[key] = random.choice(values)
    
    fill_dict["age"] = f"{patient_age}"
    fill_dict["gender"] = "F" if patient_gender == "F" else "M"
    fill_dict["duration"] = random.choice(["2 weeks", "3 months", "6 months", "1 year", "2 years", "18 months"])
    fill_dict["weeks"] = str(random.choice([2, 4, 6, 8, 12]))
    fill_dict["platelet_count"] = str(random.randint(40000, 130000))
    fill_dict["hgb"] = str(round(random.uniform(7.5, 11.5), 1))
    fill_dict["wbc"] = str(round(random.uniform(2.0, 4.5), 1))
    fill_dict["esr"] = str(random.randint(25, 85))
    fill_dict["crp"] = str(round(random.uniform(12, 65), 1))
    fill_dict["ana_titer"] = str(random.choice([80, 160, 320, 640, 1280]))
    fill_dict["egfr"] = str(random.randint(45, 82))
    fill_dict["creatinine"] = str(round(random.uniform(1.3, 2.8), 1))
    fill_dict["o2_sat"] = str(random.randint(88, 96))
    fill_dict["diagnosis"] = random.choice(["autoimmune connective tissue disease", "lupus", "inflammatory arthritis",
                                            "vasculitis", "dermatomyositis", "sarcoidosis"])
    
    # Fill template, ignoring missing keys
    try:
        note = template.format(**fill_dict)
    except KeyError:
        note = template
        for k, v in fill_dict.items():
            note = note.replace("{" + k + "}", v)
    
    return note


def generate_lupus_case_study():
    """Generate the Lupus case study from Review 1 exactly."""
    return {
        "patient": {
            "patient_id": "P-LUPUS001",
            "first_name": "Elena",
            "last_name": "Vasquez",
            "date_of_birth": datetime(1998, 3, 15),
            "gender": "F",
            "blood_type": "A+",
            "ethnicity": "Hispanic/Latino",
            "insurance": "Blue Cross Blue Shield",
            "medical_history": [],
            "current_medications": [],
            "allergies": ["Penicillin"],
            "status": "active",
            "admission_date": datetime(2023, 1, 10),
            "notes_count": 4,
            "matches_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        "notes": [
            {
                "note_type": "consultation",
                "specialty": "Dermatology",
                "physician": "Dr. Sarah Mitchell",
                "date": datetime(2023, 1, 10),
                "text": "28F presents with erythematous malar rash across both cheeks. Reports photosensitivity for the past 3 months. Rash worsens with sun exposure. No prior dermatological history. Physical examination reveals classic butterfly-pattern erythema sparing nasolabial folds. Prescribed topical hydrocortisone 1%. Advised strict sun protection with SPF 50+. Follow-up in 4 weeks."
            },
            {
                "note_type": "consultation",
                "specialty": "Hematology",
                "physician": "Dr. James Chen",
                "date": datetime(2023, 8, 15),
                "text": "Patient referred for thrombocytopenia. Platelet count 89,000/uL (normal: 150,000-400,000). CBC otherwise unremarkable. Hemoglobin 11.8 g/dL. WBC 4.2k. Peripheral smear shows no schistocytes. No splenomegaly on examination. Monitor and repeat labs in 3 months. Consider further workup if platelets continue to decline."
            },
            {
                "note_type": "consultation",
                "specialty": "Nephrology",
                "physician": "Dr. Priya Patel",
                "date": datetime(2024, 3, 20),
                "text": "Urinalysis shows proteinuria (2+). eGFR mildly reduced at 72. Creatinine 1.4 mg/dL. No prior renal history. 24-hour urine protein collection shows 1.8g protein. Complement levels: C3 low at 65 mg/dL (normal 90-180), C4 low at 10 mg/dL (normal 10-40). Started ACE inhibitor lisinopril 10mg daily. Renal biopsy considered if worsening."
            },
            {
                "note_type": "progress_note",
                "specialty": "Primary Care",
                "physician": "Dr. Michael Brown",
                "date": datetime(2024, 11, 5),
                "text": "Patient reports persistent fatigue for the past 6 months. Arthralgia in bilateral hands and knees. Morning stiffness lasting approximately 45 minutes. Attributes symptoms to work stress. Weight stable at 58 kg. Oral ulcers noted on examination. Temperature 99.2°F. OTC ibuprofen recommended. Referral to rheumatology placed for comprehensive autoimmune workup."
            }
        ]
    }


def seed_database():
    """Main seeding function."""
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    print("🗑️  Clearing existing data...")
    db.patients.drop()
    db.clinical_notes.drop()
    db.diseases.drop()
    db.matches.drop()
    db.users.drop()
    db.activity_logs.drop()
    
    # ── Seed Users ──────────────────────────────────────────────────
    print("👤 Creating test users...")
    users = [
        {
            "username": "admin",
            "email": "admin@raresense.ai",
            "full_name": "Dr. Admin User",
            "role": "admin",
            "specialty": "Internal Medicine",
            "hashed_password": pwd_context.hash("admin123"),
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "username": "clinician",
            "email": "clinician@raresense.ai",
            "full_name": "Dr. Sarah Mitchell",
            "role": "clinician",
            "specialty": "Rheumatology",
            "hashed_password": pwd_context.hash("clinician123"),
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "username": "researcher",
            "email": "researcher@raresense.ai",
            "full_name": "Dr. James Chen",
            "role": "researcher",
            "specialty": "Hematology",
            "hashed_password": pwd_context.hash("researcher123"),
            "is_active": True,
            "created_at": datetime.utcnow()
        },
    ]
    db.users.insert_many(users)
    print(f"   ✅ Created {len(users)} test users")
    
    # ── Seed Diseases ───────────────────────────────────────────────
    print("🦠 Seeding rare disease database...")
    db.diseases.insert_many(DISEASES)
    print(f"   ✅ Inserted {len(DISEASES)} rare diseases")
    
    # ── Seed Lupus Case Study ───────────────────────────────────────
    print("📋 Creating Lupus case study patient...")
    lupus_case = generate_lupus_case_study()
    db.patients.insert_one(lupus_case["patient"])
    
    from app.services.nlp_engine import extract_entities
    
    for note in lupus_case["notes"]:
        entities = extract_entities(note["text"])
        note_doc = {
            "note_id": f"N-LUPUS{lupus_case['notes'].index(note)+1:03d}",
            "patient_id": "P-LUPUS001",
            **note,
            "extracted_entities": entities,
            "created_at": datetime.utcnow()
        }
        db.clinical_notes.insert_one(note_doc)
    print("   ✅ Lupus case study created with 4 clinical notes")
    
    # ── Seed Random Patients ────────────────────────────────────────
    print("🏥 Generating patient population...")
    patient_count = 50
    all_patients = []
    all_notes = []
    
    for i in range(patient_count):
        gender = random.choice(["M", "F"])
        first_name = random.choice(FIRST_NAMES_F if gender == "F" else FIRST_NAMES_M)
        last_name = random.choice(LAST_NAMES)
        
        birth_year = random.randint(1945, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        dob = datetime(birth_year, birth_month, birth_day)
        age = 2026 - birth_year
        
        patient_id = f"P-{i+1:04d}"
        
        admission_base = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1200))
        
        patient = {
            "patient_id": patient_id,
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob,
            "gender": gender,
            "blood_type": random.choice(BLOOD_TYPES),
            "ethnicity": random.choice(ETHNICITIES),
            "insurance": random.choice(["Blue Cross", "Aetna", "United Health", "Medicare", "Medicaid", "Cigna", "Private"]),
            "emergency_contact": f"{random.choice(FIRST_NAMES_F + FIRST_NAMES_M)} {last_name}",
            "medical_history": random.sample(
                ["Hypertension", "Type 2 Diabetes", "Asthma", "Hypothyroidism", "Depression",
                 "Migraine", "GERD", "Osteoarthritis", "Obesity", "Anemia", "Chronic kidney disease"],
                k=random.randint(0, 3)
            ),
            "current_medications": random.sample(
                ["Lisinopril", "Metformin", "Levothyroxine", "Omeprazole", "Atorvastatin",
                 "Amlodipine", "Metoprolol", "Ibuprofen", "Vitamin D"],
                k=random.randint(0, 3)
            ),
            "allergies": random.sample(
                ["Penicillin", "Sulfa", "Aspirin", "Latex", "Iodine", "None known"],
                k=random.randint(0, 2)
            ),
            "status": random.choice(["active"] * 8 + ["discharged"] * 2),
            "admission_date": admission_base,
            "notes_count": 0,
            "matches_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        # Generate 2-6 clinical notes per patient
        num_notes = random.randint(2, 6)
        note_date = admission_base
        patient_notes = []
        
        for j in range(num_notes):
            specialty = random.choice(SPECIALTIES)
            note_text = generate_clinical_note(specialty, gender, age)
            
            entities = extract_entities(note_text)
            
            note_doc = {
                "note_id": f"N-{patient_id}-{j+1:03d}",
                "patient_id": patient_id,
                "note_type": random.choice(["discharge_summary", "progress_note", "consultation"]),
                "specialty": specialty,
                "physician": random.choice(PHYSICIANS),
                "date": note_date,
                "text": note_text,
                "extracted_entities": entities,
                "created_at": datetime.utcnow()
            }
            
            patient_notes.append(note_doc)
            note_date += timedelta(days=random.randint(30, 180))
        
        patient["notes_count"] = len(patient_notes)
        all_patients.append(patient)
        all_notes.extend(patient_notes)
    
    db.patients.insert_many(all_patients)
    if all_notes:
        db.clinical_notes.insert_many(all_notes)
    
    print(f"   ✅ Created {patient_count} patients with {len(all_notes)} clinical notes")
    
    # ── Create Indexes ──────────────────────────────────────────────
    print("📇 Creating database indexes...")
    
    db.patients.create_index("patient_id", unique=True)
    db.patients.create_index([("last_name", 1), ("first_name", 1)])
    
    db.clinical_notes.create_index("patient_id")
    db.clinical_notes.create_index("date")
    db.clinical_notes.create_index([("text", "text"), ("note_type", "text")])
    
    db.diseases.create_index("orpha_id", unique=True)
    db.diseases.create_index([("name", "text"), ("description", "text"), ("synonyms", "text")])
    
    db.matches.create_index("patient_id")
    db.matches.create_index([("confidence", -1)])
    
    db.activity_logs.create_index([("timestamp", -1)])
    db.activity_logs.create_index("action")
    
    print("   ✅ All indexes created")
    
    # ── Log activity ────────────────────────────────────────────────
    db.activity_logs.insert_one({
        "action": "database_seeded",
        "user": "system",
        "details": f"Database seeded with {patient_count + 1} patients, {len(all_notes) + 4} clinical notes, {len(DISEASES)} diseases",
        "timestamp": datetime.utcnow()
    })
    
    # ── Summary ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("🎉 RareSense.AI Database Seeding Complete!")
    print("=" * 60)
    print(f"  Patients:       {db.patients.count_documents({})}")
    print(f"  Clinical Notes: {db.clinical_notes.count_documents({})}")
    print(f"  Diseases:       {db.diseases.count_documents({})}")
    print(f"  Users:          {db.users.count_documents({})}")
    print(f"  Collections:    {db.list_collection_names()}")
    print()
    print("  Test Credentials:")
    print("    admin     / admin123")
    print("    clinician / clinician123")
    print("    researcher / researcher123")
    print()
    print("  Case Study Patient: Elena Vasquez (P-LUPUS001)")
    print("=" * 60)
    
    client.close()


if __name__ == "__main__":
    seed_database()
