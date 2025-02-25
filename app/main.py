from fastapi import FastAPI
import models
import database
from routers import custom_auth, core_ams

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(custom_auth.router)
app.include_router(core_ams.router)


