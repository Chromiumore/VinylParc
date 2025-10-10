from fastapi import APIRouter, Depends, HTTPException
from authx import RequestToken
from ..database import db_helper
from ..models import Musician
from ..schemas import MusicianSchema
from ..auth import auth


router = APIRouter(tags=['musicians'])


@router.get('/musicians')
def get_all_musicians():
    with db_helper.session_maker() as session:
        musicians = session.query(Musician).all()
        return musicians


@router.get('/musicians/{id}')
def get_musician(id: int):
    with db_helper.session_maker() as session:
        musician = session.query(Musician).filter_by(id=id).first()
        return musician


@router.post('/musicians/', status_code=201)
def add_musician(musician_data: MusicianSchema):
    with db_helper.session_maker() as session:
        musician = Musician(
            name=musician_data.name,
            about=musician_data.about,
            musician_type=musician_data.musician_type,
        )
        session.add(musician)
        session.commit()
        return musician.id


@router.put('/musicians/{id}')
def update_musician(id: int, musician_data: MusicianSchema):
    with db_helper.session_maker() as session:
        musician = session.query(Musician).filter_by(id=id).first()
        for key, value in musician_data.model_dump().items():
            setattr(musician, key, value)
        session.commit()
        session.refresh(musician)
        return musician


@router.delete('/musicians/{id}/')
def delete_musician(id: int):
    with db_helper.session_maker() as session:
        session.query(Musician).filter_by(id=id).delete()
        session.commit()