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


def insert_site(request: schemas.SiteBase, db: Session):
    errors = {}
    existing_site = db.query(models.Site).filter(models.Site.isdeleted == False,
                                                 models.Site.owner_user_id == request.owner_user_id,
                                                 models.Site.sitename == request.sitename,
                                                 ).first()

    if existing_site:
        errors["sitename"] = f'sitename already added'
    if errors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=errors)

    new_user_type = models.Site(**request.model_dump())
    db.add(new_user_type)
    db.commit()
    db.refresh(new_user_type)
    return new_user_type
