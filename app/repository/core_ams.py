from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas, hashing
from sqlalchemy import and_


def insert_user_type(request: schemas.UserTypeBase, db: Session):
    errors = {}
    existing_type = db.query(models.UserType).filter(models.UserType.isdeleted == False,
                                                     models.UserType.typename == request.typename).first()

    if existing_type:
        errors["typename"] = f'Type name already added'
    if errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors)

    new_user_type = models.UserType(**request.model_dump())
    db.add(new_user_type)
    db.commit()
    db.refresh(new_user_type)
    return new_user_type
