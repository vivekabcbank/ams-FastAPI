from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import app_token
from pdb import set_trace

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/custom_auth/signin-user/")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return app_token.verify_token(data, credentials_exception)