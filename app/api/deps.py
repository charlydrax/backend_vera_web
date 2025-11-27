from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.security.security import decode_token
from app.models import user as user_models
from fastapi import HTTPException, status
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    if token is None:
        return None  # utilisateur non connecté
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        return None  # token invalide -> pas de user
    result = await db.execute(select(user_models.User).filter(user_models.User.id == user_id))
    user = result.scalars().first()
    return user  # peut être None si user non trouvé
