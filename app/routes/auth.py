from fastapi import APIRouter, HTTPException, Depends, Request
from app.database import get_db
from app.models.user import UserCreate, UserLogin
from app.core.auth import get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.core.limiter import limiter


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
@limiter.limit("10/minute")
def register(request:Request, user: UserCreate):
    db = get_db()
    
    if db.users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=400,
            detail="User already exists. Please login."
        )

    hashed = hash_password(user.password)

    db.users.insert_one({
        "email": user.email,
        "password": hashed
    })

    return {"message": "User created"}

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin):
    db = get_db()
    db_user = db.users.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please register."
        )

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Wrong credentials."
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}