from fastapi import FastAPI, Request
from app import models, database
from app.routers import custom_auth, core_ams
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(custom_auth.router)
app.include_router(core_ams.router)

session = sessionmaker(bind=database.engine)()


# Create a custom exception handler for RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract errors from the validation exception
    errors = []
    for error in exc.errors():
        # Modify the error message or structure here
        field = error["loc"][-1]  # Get the field that failed validation
        message = error["msg"]  # Get the error message
        input_value = error["input"]  # Get the invalid input value

        # Customize the error message for each field
        errors.append({
            "field": field,
            "message": f"Invalid value for '{field}': {message}. Received: {input_value}"
        })

    # Return a custom error response with the formatted error message
    return JSONResponse(
        status_code=400,
        content={"detail": errors}
    )