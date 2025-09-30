from fastapi import FastAPI
from .database import db_helper

app = FastAPI()

@app.get('/')
def root_test():
    return {'message': 'Hello World'}