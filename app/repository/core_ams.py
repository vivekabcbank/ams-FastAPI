from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas, hashing
from sqlalchemy import and_
from ..allfunctions import *
from pdb import set_trace


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


def get_all_user_types(db: Session):
    user_types = db.query(models.UserType).all()
    return user_types


def get_sites(id, user_type, db: Session):
    errors = {}
    # set_trace()
    try:
        owner_user_id = decode_id(id)
        check_user = db.query(models.User).filter(models.User.isdeleted == False,
                                                  models.User.id == owner_user_id).first()
        if not check_user:
            errors["owner_user_id"] = "invalid owner_user_id"
    except Exception as e:
        errors["owner_user_id"] = "invalid owner_user_id"

    try:
        user_type = decode_id(user_type)
        check_user_type = db.query(models.UserType).filter(models.UserType.isdeleted == False,
                                                           models.UserType.id == user_type).first()
        if not check_user_type:
            errors["user_type"] = "invalid user_type"

    except Exception as e:
        errors["user_type"] = "invalid user_type"

    if user_type == User_Type_id.ADMIN.value:
        sites = db.query(models.Site).filter(models.Site.isdeleted == False,
                                             models.Site.owner_user_id == owner_user_id
                                             ).all()
    else:
        user = db.query(models.Employee).filter(models.Employee.id == owner_user_id).first()

        if not user:
            errors["eployee_404"] = "Employee not found"

        sites = user.site_info

        if not sites:
            errors["eployee_404_no_sites"] = "Employee has no site information"
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    return sites


def get_employee(site_info_id, db: Session):
    errors = {}
    try:
        site_info_id = decode_id(site_info_id)
        check_sites = db.query(models.Site).filter(models.Site.isdeleted == False,
                                                   models.Site.id == site_info_id).first()
        if not check_sites:
            errors["site_info_id"] = "invalid site_info_id"
    except Exception as e:
        errors["site_info_id"] = "invalid site_info_id"

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    employees = db.query(models.Employee).filter(models.Employee.isdeleted == False,
                                                 models.Employee.site_info_id == site_info_id
                                                 ).all()
    return employees
