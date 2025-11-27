from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message

async def create_message(db: AsyncSession, user_id: int, role: str, content: str):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_user_messages(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Message).where(Message.user_id == user_id).order_by(Message.created_at)
    )
    return result.scalars().all()
