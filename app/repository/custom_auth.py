from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas, hashing, token
from sqlalchemy import and_


def insertEmployee(request: schemas.EmployeeBase, db: Session):
    errors = {}

    existing_user = db.query(models.User).filter(
        and_(
            models.User.calling_code == request.calling_code,
            models.User.phone == request.phone,
            models.User.isdeleted == False
        )
    ).first()

    if existing_user:
        errors["invalid_phone"] = f'Phone is already in use1.'

    email_user = db.query(models.User).filter(models.User.isdeleted == False,
                                              models.User.email == request.email).first()

    if email_user:
        errors["invalid_email"] = f'Email is already in use2.'

    user_type = db.query(models.UserType).filter(models.UserType.isdeleted == False,
                                                 models.UserType.id == int(request.usertype_id)).first()

    if not user_type:
        errors["usertype_id"] = f'Invalid user type'

    site_info = db.query(models.Site).filter(models.Site.isdeleted == False,
                                             models.Site.id == int(request.site_info_id)).first()

    # if not site_info:
    #     errors["site_info_id"] = f'Invalid site info'

    if errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors)

    new_user = models.User(
        company_name=request.company_name,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        username=request.username,
        usertype_id=request.usertype_id,
        image=request.image,
        gender=request.gender,
        dob=request.dob,
        calling_code=request.calling_code,
        phone=request.phone,
        address=request.address,
        pincode=request.pincode,
        country=request.country,
        state=request.state,
        city=request.city
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_employee = models.Employee(
        user=new_user,
        site_info_id=request.site_info_id,
        joiningdate=request.joiningdate,
        min_wages=request.min_wages,
        qualification=request.qualification,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def userSignin(request: schemas.Login, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    errors = {}
    if not user:
        errors["password"] = "Wrong username"
    elif not hashing.Hash.verify(request.password, user.password):
        errors["password"] = "Wrong password"

    if errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors)

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def userSignUp(request: schemas.UserBase, db: Session):
    errors = {}

    existing_user = db.query(models.User).filter(
        and_(
            models.User.calling_code == request.calling_code,
            models.User.phone == request.phone,
            models.User.isdeleted == False
        )
    ).first()

    if existing_user:
        errors["invalid_phone"] = f'Phone is already in use1.'

    email_user = db.query(models.User).filter(models.User.isdeleted == False,
                                              models.User.email == request.email).first()

    if email_user:
        errors["invalid_email"] = f'Email is already in use2.'

    if errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors)

    new_user = models.User(**request.model_dump())
    new_user.password = hashing.Hash.bcrypt(request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
