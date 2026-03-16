from fastapi import APIRouter, Depends, HTTPException
from schamas.user import UserCreate
from database import get_db
from models.user import User
from security.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/register")
def create_users(user: UserCreate, db=Depends(get_db)):
    user_exist = db.query(User).filter(User.username == user.username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="User already exist")
    else:
        # new_user = User(**user.model_dump()) // this is for plain password
        new_user = User(
            username=user.username,
            password=hash_password(user.password)
        )        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}
               
    
@router.post("/login")
def user_login(user: UserCreate, db=Depends(get_db)):
    user_exist = db.query(User).filter(User.username == user.username).first()
    if not user_exist:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not verify_password(user.password, user_exist.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = create_access_token({'sub': user_exist.username})
    return {"token": access_token, "token_type": "bearer"}

@router.post("/token")
def get_token(form_data:OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user_exist = db.query(User).filter(User.username == form_data.username).first()
    if not user_exist:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not verify_password(form_data.password, user_exist.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = create_access_token({'sub': user_exist.username})
    return {"access_token": access_token, "token_type": "bearer"}
    
    