from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, messages, results
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv
from typing import List, Dict, Any
import os
import httpx
from fastapi import HTTPException
from pathlib import Path

# Charger .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="MyApp API")

# CORS — autoriser Angular (dev + prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://vera-front-git-main-celias-projects-19b36730.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES EXISTANTES
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])
app.include_router(results.router, prefix="/api/v1", tags=["results"])

@app.get("/api/v1/survey/results")
async def get_survey_results() -> List[Dict[str, Any]]:
    """
    Récupère les résultats du Google Form via l'API Google Sheets
    et les renvoie sous forme de liste de lignes { "colonne": valeur }.
    """

    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
    sheet_range = os.getenv("GOOGLE_SHEETS_RANGE")  # ex: "Réponses au formulaire 1!A1:Z1000"
    api_key = os.getenv("GOOGLE_SHEETS_API_KEY")

    if not spreadsheet_id or not sheet_range or not api_key:
        raise HTTPException(
            status_code=500,
            detail="Configuration Google Sheets manquante (ID, RANGE ou API KEY).",
        )

    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/"
        f"{spreadsheet_id}/values/{sheet_range}?key={api_key}"
    )

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur Google Sheets: {resp.status_code} - {resp.text}",
        )

    data = resp.json()
    values = data.get("values", [])

    if not values:
        return []

    # Première ligne = en-têtes (noms de colonnes == questions du Google Form)
    headers = values[0]
    rows: List[Dict[str, Any]] = []

    for i, row in enumerate(values[1:], start=2):
        row_dict: Dict[str, Any] = {"row_number": i}
        for idx, header in enumerate(headers):
            # Si la ligne est plus courte que le nombre de colonnes
            value = row[idx] if idx < len(row) else None
            row_dict[header] = value
        rows.append(row_dict)

    return rows



# Initialisation async des tables
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
