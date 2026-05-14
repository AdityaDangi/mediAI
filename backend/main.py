from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from database import engine, Base
from auth import router as auth_router
from rag import router as rag_router
from skin import router as skin_router
from patients import router as patients_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical AI Platform", version="1.0.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS if o.strip()]

# Always allow localhost for local development
DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEFAULT_ORIGINS + ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(skin_router)
app.include_router(patients_router)

@app.get("/")
def root():
    return {"message": "Medical AI Platform API is running"}
