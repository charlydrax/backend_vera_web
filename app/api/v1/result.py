from fastapi import APIRouter
import httpx
from urllib.parse import quote
from app.core.config import settings
from typing import List, Dict, Optional


router = APIRouter(prefix="/survey", tags=["survey"])


async def _fetch_survey_results():
    # Encode les espaces et accents
    encoded_range = quote(settings.GOOGLE_SHEETS_RANGE, safe="!'")

    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/"
        f"{settings.GOOGLE_SHEETS_SPREADSHEET_ID}/values/{encoded_range}"
        f"?key={settings.GOOGLE_SHEETS_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        resp.raise_for_status()

    data = resp.json()
    values = data.get("values", [])

    if not values:
        return []

    headers = values[0]  # La 1ère ligne : Horodateur, Parlons de toi..., etc.
    rows = values[1:]    # Les réponses

    results = [
        {
            headers[i]: row[i] if i < len(row) else None
            for i in range(len(headers))
        }
        for row in rows
    ]

    return results


@router.get("/results", response_model=List[Dict[str, Optional[str]]])
async def get_results():
    return await _fetch_survey_results()