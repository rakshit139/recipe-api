from bson import ObjectId
from fastapi import HTTPException

def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    return id
