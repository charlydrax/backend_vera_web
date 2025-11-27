from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="MyApp API")

# CORS — autoriser Angular (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # adapter pour prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# Initialisation async des tables
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
