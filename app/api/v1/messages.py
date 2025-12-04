from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
import httpx
import os
from app.crud.message import create_message  # pour enregistrer si user connecté
from app.schemas.message import MessageRequest
from app.core.config import settings
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", tags=["messages"])


# @router.post("/ask")
# async def ask_vera(msg: MessageRequest, db: AsyncSession = Depends(get_db)):
#     try:
#         async with httpx.AsyncClient() as client:
#             payload = {"userId": "anon", "query": msg.message}
#             headers = {
#                 "X-API-Key": settings.VERA_API_KEY,
#                 "Content-Type": "application/json"
#             }
#             response = await client.post(settings.VERA_ENDPOINT, json=payload, headers=headers)
#             response.raise_for_status()
#             vera_response = response.text
#     except Exception as e:
#         # log(e) si tu veux
#         vera_response = '{"answer": "Vera est momentanément indisponible, mais ton backend fonctionne bien 🎉"}'

#     return vera_response
@router.post("/ask")
async def ask_vera(
    msg: MessageRequest,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Proxy entre le front Vera et l’API Vera externe.

    - Reçoit { "message": "..."}
    - Appelle l’API Vera avec userId + query
    - Normalise la réponse pour toujours renvoyer un JSON du type { "answer": "..." }
    """

    # 1) Appel à l’API Vera externe
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            payload = {
                "userId": "anon",          # tu pourras mettre un vrai userId plus tard
                "query": msg.message,
            }
            headers = {
                "X-API-Key": settings.VERA_API_KEY,
                "Content-Type": "application/json",
            }

            upstream_resp = await client.post(
                settings.VERA_ENDPOINT,
                json=payload,
                headers=headers,
            )
    except httpx.HTTPError as e:
        # Erreur réseau / timeout / DNS, etc.
        logger.error("Erreur réseau en appelant VERA_ENDPOINT", exc_info=e)
        return {
            "answer": "Vera est momentanément indisponible (problème de connexion au serveur). "
                      "Tu peux réessayer dans quelques instants."
        }

    # 2) Status code non OK (401, 403, 404, 500…)
    if not upstream_resp.ok:
        logger.error(
            "Réponse non OK de VERA_ENDPOINT (%s): %s",
            upstream_resp.status_code,
            upstream_resp.text,
        )
        return {
            "answer": "Vera a répondu avec une erreur technique. "
                      "On regarde ce qui se passe, réessaie un peu plus tard."
        }

    # 3) Tentative de JSON
    try:
        data = upstream_resp.json()
    except ValueError:
        # Réponse non JSON : on renvoie le texte brut quand même
        logger.warning("Réponse non-JSON de Vera: %s", upstream_resp.text)
        return {
            "answer": upstream_resp.text or "Vera a répondu, mais dans un format inattendu."
        }

    # 4) Normalisation : on essaie de récupérer un champ cohérent
    answer = (
        data.get("answer")
        or data.get("response")
        or data.get("output")
        or str(data)
    )

    return {"answer": answer}