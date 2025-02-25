from fastapi import APIRouter

router = APIRouter(
    tags=["custom_auth"],
    prefix="/custom_auth"
)

@router.post("/signup-user/")
def userSignUpView():
    return "hi"

@router.post("/signin-user/")
def userSigninView():
    return "hi"

@router.post("/insert-employee/")
def insertEmployeeView():
    return "hi"

