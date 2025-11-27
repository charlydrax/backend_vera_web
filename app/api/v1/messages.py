from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.message import MessageCreate, MessageOut
from app.crud.message import create_message, get_user_messages
from app.api.deps import get_current_user  # dépendant token

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=MessageOut)
async def add_message(msg: MessageCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await create_message(db, user.id, msg.role, msg.content)


@router.get("/", response_model=list[MessageOut])
async def list_messages(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await get_user_messages(db, user.id)
