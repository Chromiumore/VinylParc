from fastapi import FastAPI
from .routers.records import router as records_router
from .routers.compositions import router as compositions_router

def create_app():
    app = FastAPI()
    app.include_router(records_router)
    app.include_router(compositions_router)

    return app
