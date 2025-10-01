from fastapi import APIRouter
from ..database import db_helper
from ..models import Composition
from ..schemas import CompositionSchema

router = APIRouter()


@router.get('/compositions')
def get_all_compositions():
    with db_helper.session_maker() as session:
        compositions = session.query(Composition).all()
        return compositions
    

@router.get('/compositions/{id}')
def get_composition(id: int):
    with db_helper.session_maker() as session:
        record = session.query(Composition).filter_by(id=id).first()
        return record


@router.post('/compositions/', status_code=201)
def add_composition(composition_data: CompositionSchema):
    with db_helper.session_maker() as session:
        composition = Composition(
            name=composition_data.name,
            about=composition_data.about,
        )
        session.add(composition)
        session.commit()
        return composition.id


@router.put('/compositions/{id}')
def update_composition(id: int, composition_data: CompositionSchema):
    with db_helper.session_maker() as session:
        composition = session.query(Composition).filter_by(id=id).first()
        for key, value in composition_data.model_dump().items():
            setattr(composition, key, value)
        session.commit()
        session.refresh(composition)
        return composition


@router.delete('/compositions/{id}/')
def delete_composition(id: int):
    with db_helper.session_maker() as session:
        session.query(Composition).filter_by(id=id).delete()
        session.commit()
