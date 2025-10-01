from fastapi import FastAPI
from .routers.records import router as records_router
from .routers.compositions import router as compositions_router
from .routers.musicians import router as musicians_router
from .routers.ensembles import router as ensembles_router
from .routers.performances import router as performances_roter
from .auth import router as auth_router

def create_app():
    app = FastAPI()
    app.include_router(records_router)
    app.include_router(compositions_router)
    app.include_router(musicians_router)
    app.include_router(ensembles_router)
    app.include_router(performances_roter)
    app.include_router(auth_router)

    return app
