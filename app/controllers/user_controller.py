
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config_db.session import get_db
from app.schemas.token_schema import TokenSchema
from app.security_pack.auth import verify_creds_and_return_user,create_access_token



router = APIRouter(prefix="/login", tags=["login1x"])

@router.post("/createtoken", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Create a new access token for the user.
    """
    is_valid, user = verify_creds_and_return_user(form_data, db)
    if is_valid:
        access_token = create_access_token(user)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="xx Invalid username or password")



