import httpx
from app.core.config import settings


async def ask_vera(query: str, user_id="anon"):
    async with httpx.AsyncClient(timeout=30) as client:
        payload = {
            "userId": f"user_{user_id}",
            "query": query
        }
        headers = {
            "X-API-Key": settings.VERA_API_KEY,
            "Content-Type": "application/json"
        }

        response = await client.post(settings.VERA_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.text
