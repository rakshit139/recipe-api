from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from app.core.deps import oauth2_scheme
from app.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    db = get_db()
    user = db.users.find_one({"email": email})

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return user
