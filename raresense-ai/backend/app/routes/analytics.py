"""
RareSense.AI — Analytics Routes (Week 3)
Aggregation pipelines for dashboard insights
"""
from fastapi import APIRouter
from datetime import datetime, timedelta

from app.config import mongo

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard_stats():
    """Get overall dashboard statistics using aggregation pipelines."""
    # Basic counts
    total_patients = await mongo.db.patients.count_documents({})
    total_notes = await mongo.db.clinical_notes.count_documents({})
    total_diseases = await mongo.db.diseases.count_documents({})
    total_matches = await mongo.db.matches.count_documents({})
    active_patients = await mongo.db.patients.count_documents({"status": "active"})
    
    # Average confidence of matches
    avg_pipeline = [
        {"$group": {
            "_id": None,
            "avg_confidence": {"$avg": "$confidence"},
            "max_confidence": {"$max": "$confidence"},
            "min_confidence": {"$min": "$confidence"}
        }}
    ]
    avg_result = None
    async for doc in mongo.db.matches.aggregate(avg_pipeline):
        avg_result = doc
    
    # Recent activity count (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(hours=24)
    recent_activity = await mongo.db.activity_logs.count_documents(
        {"timestamp": {"$gte": yesterday}}
    )
    
    return {
        "total_patients": total_patients,
        "active_patients": active_patients,
        "total_notes": total_notes,
        "total_diseases": total_diseases,
        "total_matches": total_matches,
        "recent_activity_24h": recent_activity,
        "avg_confidence": round(avg_result["avg_confidence"] * 100, 1) if avg_result else 0,
        "max_confidence": round(avg_result["max_confidence"] * 100, 1) if avg_result else 0,
        "min_confidence": round(avg_result["min_confidence"] * 100, 1) if avg_result else 0,
    }


@router.get("/symptom-frequency")
async def get_symptom_frequency():
    """Get most common extracted symptoms using $unwind and $group."""
    pipeline = [
        {"$unwind": "$extracted_entities"},
        {"$match": {"extracted_entities.entity_type": "symptom"}},
        {"$group": {
            "_id": "$extracted_entities.normalized_name",
            "count": {"$sum": 1},
            "hpo_code": {"$first": "$extracted_entities.hpo_code"},
            "avg_confidence": {"$avg": "$extracted_entities.confidence"}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 20},
        {"$project": {
            "symptom": "$_id",
            "count": 1,
            "hpo_code": 1,
            "avg_confidence": {"$round": ["$avg_confidence", 3]},
            "_id": 0
        }}
    ]
    
    symptoms = []
    async for doc in mongo.db.clinical_notes.aggregate(pipeline):
        symptoms.append(doc)
    
    return {"symptoms": symptoms}


@router.get("/disease-distribution")
async def get_disease_distribution():
    """Get disease category breakdown using $facet."""
    pipeline = [
        {"$facet": {
            "by_category": [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"category": "$_id", "count": 1, "_id": 0}}
            ],
            "by_prevalence": [
                {"$group": {"_id": "$prevalence", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"prevalence": "$_id", "count": 1, "_id": 0}}
            ],
            "by_inheritance": [
                {"$group": {"_id": "$inheritance", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"inheritance": "$_id", "count": 1, "_id": 0}}
            ],
            "total": [
                {"$count": "count"}
            ]
        }}
    ]
    
    result = None
    async for doc in mongo.db.diseases.aggregate(pipeline):
        result = doc
    
    return result or {"by_category": [], "by_prevalence": [], "by_inheritance": [], "total": [{"count": 0}]}


@router.get("/timeline-density")
async def get_timeline_density():
    """Get visit density over time using $dateToString and $group."""
    pipeline = [
        {"$group": {
            "_id": {
                "$dateToString": {"format": "%Y-%m", "date": "$date"}
            },
            "visit_count": {"$sum": 1},
            "unique_patients": {"$addToSet": "$patient_id"},
            "entity_count": {"$sum": {"$size": {"$ifNull": ["$extracted_entities", []]}}}
        }},
        {"$project": {
            "month": "$_id",
            "visit_count": 1,
            "patient_count": {"$size": "$unique_patients"},
            "entity_count": 1,
            "_id": 0
        }},
        {"$sort": {"month": 1}}
    ]
    
    density = []
    async for doc in mongo.db.clinical_notes.aggregate(pipeline):
        density.append(doc)
    
    return {"timeline": density}


@router.get("/match-accuracy")
async def get_match_accuracy():
    """Get matching engine performance statistics using aggregation."""
    pipeline = [
        {"$facet": {
            "confidence_buckets": [
                {"$bucket": {
                    "groupBy": "$confidence",
                    "boundaries": [0, 0.2, 0.4, 0.6, 0.8, 1.01],
                    "default": "Other",
                    "output": {
                        "count": {"$sum": 1},
                        "diseases": {"$addToSet": "$disease_name"}
                    }
                }}
            ],
            "by_status": [
                {"$group": {"_id": "$status", "count": {"$sum": 1}}},
                {"$project": {"status": "$_id", "count": 1, "_id": 0}}
            ],
            "top_diseases": [
                {"$group": {
                    "_id": "$disease_name",
                    "match_count": {"$sum": 1},
                    "avg_confidence": {"$avg": "$confidence"}
                }},
                {"$sort": {"match_count": -1}},
                {"$limit": 10},
                {"$project": {
                    "disease": "$_id",
                    "match_count": 1,
                    "avg_confidence": {"$round": ["$avg_confidence", 3]},
                    "_id": 0
                }}
            ],
            "overall": [
                {"$group": {
                    "_id": None,
                    "total": {"$sum": 1},
                    "avg_confidence": {"$avg": "$confidence"},
                    "avg_matched_symptoms": {"$avg": "$matched_count"}
                }}
            ]
        }}
    ]
    
    result = None
    async for doc in mongo.db.matches.aggregate(pipeline):
        result = doc
    
    return result or {"confidence_buckets": [], "by_status": [], "top_diseases": [], "overall": []}


@router.get("/recent-activity")
async def get_recent_activity(limit: int = 20):
    """Get recent activity logs."""
    cursor = mongo.db.activity_logs.find().sort("timestamp", -1).limit(limit)
    
    activities = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        activities.append(doc)
    
    return {"activities": activities}


@router.get("/entity-breakdown")
async def get_entity_breakdown():
    """Get breakdown of all extracted entity types."""
    pipeline = [
        {"$unwind": "$extracted_entities"},
        {"$group": {
            "_id": "$extracted_entities.entity_type",
            "count": {"$sum": 1},
            "avg_confidence": {"$avg": "$extracted_entities.confidence"}
        }},
        {"$project": {
            "entity_type": "$_id",
            "count": 1,
            "avg_confidence": {"$round": ["$avg_confidence", 3]},
            "_id": 0
        }},
        {"$sort": {"count": -1}}
    ]
    
    entities = []
    async for doc in mongo.db.clinical_notes.aggregate(pipeline):
        entities.append(doc)
    
    return {"entities": entities}
