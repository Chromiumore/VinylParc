from fastapi import FastAPI
from .records import router as records_router

def create_app():
    app = FastAPI()
    app.include_router(records_router)

    return app
