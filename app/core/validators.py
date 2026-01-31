from fastapi import Path, HTTPException
from bson import ObjectId

def validate_object_id(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid ID")
    return id
