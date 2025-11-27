# import httpx
# import os
# from fastapi import HTTPException
# from app.schemas.message import MessageCreate, MessageOut
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import APIRouter, Depends
# from app.crud.message import create_message, get_user_messages
# from app.db.session import get_db
# from app.api.deps import get_current_user  # dépendant token


# VERA_API_KEY = os.getenv("VERA_API_KEY")
# VERA_ENDPOINT = "https://feat-api-partner---api-ksrn3vjgma-od.a.run.app/api/v1/chat"

# # router = APIRouter(prefix="/ask", tags=["ask"])


# @router.post("/ask")
# async def ask_vera(msg: MessageCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):

#     # 1. Enregistrer le message utilisateur
#     await create_message(db, user.id, "user", msg.content)

#     # 2. Envoyer à Vera
#     payload = {
#         "userId": f"user_{user.id}",
#         "query": msg.content
#     }
#     headers = {
#         "X-API-Key": VERA_API_KEY,
#         "Content-Type": "application/json"
#     }

#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(VERA_ENDPOINT, json=payload, headers=headers)
#             response.raise_for_status()
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Erreur API Vera : {e}")

#     data = response.json()

#     # Vera répond généralement avec: "answer", "verdict", "details"
#     ai_answer = data.get("answer", "Aucune réponse")

#     # 3. Enregistrer la réponse de Vera
#     await create_message(db, user.id, "assistant", ai_answer)

#     # 4. Retourner la réponse
#     return {
#         "answer": ai_answer,
#         "verdict": data.get("verdict"),
#         "details": data.get("details"),
#     }
