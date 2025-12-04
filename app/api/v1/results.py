# api/v1/results.py

from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(
    prefix="/api/v1",
    tags=["results"],
)

@router.get("/survey/results")
async def get_survey_results() -> List[Dict[str, Any]]:
    return [
        {
            "row_number": 1,
            "Horodateur": "27/11/2025 15:25:51",
            "Parlons de toi, tu as": "18 - 25 ans",
            "Quand tu vois une info sur Instagram ou TikTok, tu as tendance à…": "Vérifier Rarement",
        },
        {
            "row_number": 2,
            "Horodateur": "27/11/2025 15:30:12",
            "Parlons de toi, tu as": "18 - 25 ans",
            "Quand tu vois une info sur Instagram ou TikTok, tu as tendance à…": "Vérifier Souvent",
        },
        {
            "row_number": 3,
            "Horodateur": "27/11/2025 15:35:44",
            "Parlons de toi, tu as": "26 - 35 ans",
            "Quand tu vois une info sur Instagram ou TikTok, tu as tendance à…": "Ne pas vérifier",
        },
    ]
