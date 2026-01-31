from fastapi import FastAPI
from app.database import get_db
from app.routes.recipe import router as recipe_router
from app.routes.auth import router as auth_router
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Recipe API",
    description="A secure Recipe API built with FastAPI + MongoDB + JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

app.state.limiter = limiter

@app.get("/")
def root():
    return {"message": "Recipe API running"}

app.include_router(auth_router)


app.include_router(recipe_router)
