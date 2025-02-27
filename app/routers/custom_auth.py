from fastapi import APIRouter, Depends, HTTPException, Request
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import custom_auth

router = APIRouter(
    tags=["auth"],
    prefix="/custom_auth"
)


@router.post("/signup-user/")
async def userSignUpView(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    return custom_auth.userSignUp(request, db)


@router.post("/signin-user/")
def userSigninView(request: schemas.Login, db: Session = Depends(database.get_db)):
    return custom_auth.userSignin(request, db)


@router.post("/insert-employee/")
def insertEmployeeView():
    return "hi"
