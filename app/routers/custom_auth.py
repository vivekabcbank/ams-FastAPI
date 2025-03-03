from fastapi import APIRouter, Depends, HTTPException, Request
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import custom_auth
from fastapi.security import OAuth2PasswordRequestForm
from .. import oauth2

router = APIRouter(
    tags=["auth"],
    prefix="/custom_auth"
)


@router.post("/signup-user/")
async def userSignUpView(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    return custom_auth.userSignUp(request, db)


# def userSigninView(request: schemas.Login, db: Session = Depends(database.get_db)):
@router.post("/signin-user/")
def userSigninView(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return custom_auth.userSignin(request, db)


@router.post("/insert-employee/")
def insertEmployeeView(request: schemas.EmployeeBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return custom_auth.insertEmployee(request, db)
