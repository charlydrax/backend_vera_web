from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
import httpx
import os
from app.crud.message import create_message  # pour enregistrer si user connecté
from app.schemas.message import MessageRequest
from app.core.config import VERA_API_KEY, VERA_ENDPOINT

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/ask")
async def ask_vera(msg: MessageRequest, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        payload = {
            "userId": f"user_{user.id}" if user else "anon",
            "query": msg.message
        }
        headers = {
            "X-API-Key": VERA_API_KEY,
            "Content-Type": "application/json"
        }
        response = await client.post(VERA_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        vera_response = response.text

    # Enregistrer seulement si user connecté
    if user:
        await create_message(db, user.id, role="user", content=msg.message)
        await create_message(db, user.id, role="vera", content=vera_response.get("answer", ""))

    return vera_response
