from pdb import set_trace

from pydantic import BaseModel, ValidationError, model_validator, field_validator, PydanticUserError, root_validator, \
    validator, constr, confloat
from pydantic import EmailStr, conint
from typing import Optional
from datetime import date
from fastapi import HTTPException
from .allfunctions import *
from sqlalchemy.orm import Session
from fastapi import Depends
from . import database
from . import models
from sqlalchemy import and_


class UserBase(BaseModel):
    company_name: constr(min_length=1, max_length=250)
    first_name: constr(min_length=1, max_length=250, pattern=r'^[a-zA-Z]+$')
    last_name: constr(min_length=1, max_length=250, pattern=r'^[a-zA-Z]+$')
    email: EmailStr
    usertype_id: constr(min_length=1, max_length=250)
    image: Optional[str] = ''
    gender: constr(min_length=1, max_length=2)
    dob: date
    calling_code: constr(min_length=1, max_length=2, pattern=r'^[0-9]*$')
    phone: constr(min_length=10, max_length=250, pattern=r'^[0-9]*$')
    address: constr(min_length=1, max_length=250)
    pincode: constr(min_length=1, max_length=250, pattern=r'^[0-9]*$')
    country: constr(min_length=1, max_length=250)
    state: constr(min_length=1, max_length=250)
    city: constr(min_length=1, max_length=250)
    password: constr(min_length=1, max_length=250)

    class Config:
        from_attributes = True

    @property
    def username(self):
        return ""

    @field_validator('gender')
    def validate_gender(cls, value):
        if value not in ['M', 'F', 'O']:
            raise ValueError("Gender must be 'M', 'F' or 'O'")
        return value

    @model_validator(mode="before")
    def check_required_fields(cls, data):
        errors = {}
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['username'] = set_username(first_name, last_name)

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        return data


class EmployeeBase(BaseModel):
    company_name: constr(min_length=1, max_length=250)
    first_name: constr(min_length=1, max_length=250, pattern=r'^[a-zA-Z]+$')
    last_name: constr(min_length=1, max_length=250, pattern=r'^[a-zA-Z]+$')
    email: EmailStr
    username: Optional[str] = ""
    gender: constr(min_length=1, max_length=2)
    dob: Optional[date]
    calling_code: constr(min_length=1, max_length=2, pattern=r'^[0-9]*$')
    phone: constr(min_length=10, max_length=250, pattern=r'^[0-9]*$')
    address: constr(min_length=1, max_length=250)
    pincode: constr(min_length=1, max_length=250, pattern=r'^[0-9]*$')
    country: constr(min_length=1, max_length=250)
    state: constr(min_length=1, max_length=250)
    city: constr(min_length=1, max_length=250)
    usertype_id: constr(min_length=1, max_length=250)
    site_info_id: constr(min_length=1, max_length=250)
    joiningdate: date
    min_wages: confloat()
    qualification: constr(min_length=1, max_length=250)
    image: Optional[str] = ''

    class Config:
        from_attributes = True

    @field_validator('gender')
    def validate_gender(cls, value):
        if value not in ['M', 'F', 'O']:
            raise ValueError("Gender must be 'M', 'F' or 'O'")
        return value

    @model_validator(mode="before")
    def check_required_fields(cls, data):
        errors = {}
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['username'] = set_username(first_name, last_name)
        try:
            data["usertype_id"] = str(decode_id(data.get("usertype_id")))
        except Exception as e:
            errors["usertype_id"] = "invalid user type id"

        try:
            data["site_info_id"] = str(decode_id(data.get("site_info_id")))
        except Exception as e:
            errors["site_info_id"] = "invalid site info id"

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        return data


class UserTypeBase(BaseModel):
    typename: constr(min_length=1, max_length=250)
    description: Optional[str]

    class Config:
        from_attributes = True


class SiteBase(BaseModel):
    owner_user_id: constr(min_length=1, max_length=250)
    sitename: constr(min_length=1, max_length=250)
    address: constr(min_length=1, max_length=250)
    country: constr(min_length=1, max_length=250)
    state: constr(min_length=1, max_length=250)
    city: constr(min_length=1, max_length=250)
    latitude: constr(min_length=1, max_length=20, pattern=r'^[0-9.]*$')
    longitude: constr(min_length=1, max_length=20, pattern=r'^[0-9.]*$')

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def check_required_fields(cls, data):
        errors = {}
        try:
            data["owner_user_id"] = str(decode_id(data.get("owner_user_id")))
        except Exception as e:
            errors["owner_user_id"] = "invalid owner_user_id"

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        return data


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str


class ShowUserType(BaseModel):
    id: int
    typename: str
    description: str

    class Config():
        from_attributes = True