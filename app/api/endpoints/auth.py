from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
 
from app.db.session import get_main_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import create_access_token, get_current_active_user
 
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
 
@router.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_main_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
 
    user = User(
        email=user_in.email,
        password_hash=pwd_context.hash(user_in.password),
        full_name=user_in.full_name,
        address=user_in.address,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
 
 
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_main_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
 
 
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user