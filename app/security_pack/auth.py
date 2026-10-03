
from datetime import datetime, timedelta, timezone
from app.config_db.settings import settings

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session 
from pwdlib import PasswordHash
from app.config_db.session import get_db
from app.models.user_model import User
import jwt 




def verify_creds_and_return_user(form_data: OAuth2PasswordRequestForm, db: Session):
    """
    Verify the user's credentials and return the user object.
    """
    # old way : db.query(User).filter(User.username == username).first()
    # new way : db.scalar(select(User).where(User.username == form_data.username))
    # Select the matching user, if one exists.

    user = db.scalar(select(User).where(User.username == form_data.username))
    if not user or not user.is_active:
        return False, None
    if not PasswordHash.recommended().verify(form_data.password, user.hashed_password):
        return False, None
    return True, user


def create_access_token(user: User) :
    """
    Create a new access token for the user.
    """
    payload = {
        "sub": str(user.id),
        "name": user.username,
        "role": user.role,
        "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.access_token_expire_minutes),
    }
    token = jwt.encode(payload, settings.access_token_secret_key, algorithm="HS256")
    return token






# The tokenUrl is metadata for OpenAPI/Swagger, 
# telling its OAuth2 interface which endpoint issues tokens. 
# It does not make oauth2_scheme call that route automatically.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/createtoken")

def verify_token_and_get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the access token.
    """
    try:
        payload = jwt.decode(token, settings.access_token_secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(user_id)
        user = db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="User not active")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    

    