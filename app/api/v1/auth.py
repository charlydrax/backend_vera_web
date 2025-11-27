from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut, Token, UserEmail, LoginRequest
from app.crud import user as crud_user
from app.db.session import get_db
from app.security.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from app.crud.user import get_all_emails


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    print("Registering user:", user_in)
    existing = await crud_user.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await crud_user.create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get('/emails', response_model=list[UserEmail])
async def list_user_emails(db: AsyncSession = Depends(get_db)):
    emails = await get_all_emails(db)  # ⬅️ important : await !
    return [{'email': e} for e in emails]  # e est déjà un str grâce à .scalars()