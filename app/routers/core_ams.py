from fastapi import APIRouter

router = APIRouter(
    tags=["core_ams"],
    prefix="/core_ams"
)


@router.get("/insert-user-type/")
def insertUserTypeView():
    return "hi"


@router.get("/insert-site/")
def insertSiteView():
    return "hi"


@router.get("/get-sites/")
def getSitesView():
    return "hi"


@router.get("/get-employee/")
def getEmployeeView():
    return "hi"


@router.post("/apply-leave/")
def applyLeaveView():
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


@router.post("/make-superviser/")
def makeSuperviserView():
    return "hi"


@router.post("/mark-attendance/")
def insertCityView():
    return "hi"


@router.post("/get-state-by-country/")
def getStateByCountry():
    return "hi"


@router.post("/get-city-by-state/")
def getCityByState():
    return "hi"


@router.post("/get-country/")
def getCountry():
    return "hi"
