from fastapi import APIRouter, Depends
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import core_ams
from typing import List

router = APIRouter(
    tags=["core"],
    prefix="/core_ams"
)


@router.post("/insert-user-type/")
def insertUserTypeView(request: schemas.UserTypeBase, db: Session = Depends(database.get_db),
                       current_user: schemas.User = Depends(oauth2.get_current_user)):
    return core_ams.insert_user_type(request, db)


@router.post("/insert-site/")
def insertSiteView(request: schemas.SiteBase, db: Session = Depends(database.get_db),
                   current_user: schemas.User = Depends(oauth2.get_current_user)):
    return core_ams.insert_site(request, db)


@router.get("/get-usertypes/", response_model=List[schemas.ShowUserType])
def getUserTypes(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return core_ams.get_all_user_types(db)


@router.get("/get-sites/{owner_user_id}/{user_type}/")
def getSitesView(id, user_type, db: Session = Depends(database.get_db),
                 current_user: schemas.User = Depends(oauth2.get_current_user)):
    return core_ams.get_sites(id, user_type, db)


@router.get("/get-employee/{site_info_id}/")
def getEmployeeView(site_info_id, db: Session = Depends(database.get_db),
                    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return core_ams.get_employee(site_info_id, db)


@router.post("/apply-leave/")
def applyLeaveView(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return "hi"


@router.post("/make-superviser/")
def makeSuperviserView(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return "hi"


@router.post("/mark-attendance/")
def markAttendanceView(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return "hi"


@router.post("/insert-country/")
def insertCountryView():
    return "hi"


@router.post("/insert-state/")
def insertStateView():
    return "hi"


@router.post("/insert-city/")
def insertCityView():
    return "hi"


@router.get("/get-state-by-country/")
def getStateByCountry():
    return "hi"


@router.get("/get-city-by-state/")
def getCityByState():
    return "hi"


@router.get("/get-country/")
def getCountry():
    return "hi"
