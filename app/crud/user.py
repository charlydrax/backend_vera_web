from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select
from app.models import user
from app.schemas import user as schemas
from app.security.security import get_password_hash
from sqlalchemy.orm import Session


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(user.User).filter(user.User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: schemas.UserCreate):
    hashed = get_password_hash(user_in.password)
    db_user = user.User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# def get_all_emails(db: Session):
#     return db.query(user.User.email).all()


async def get_all_emails(db: AsyncSession):
    result = await db.execute(select(user.User.email))
    return result.scalars().all()