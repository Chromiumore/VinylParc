from fastapi import APIRouter
from ..database import db_helper
from ..models import Ensemble
from ..schemas import EnsembleSchema


router = APIRouter(tags=['ensembles'])


@router.get('/ensembles')
def get_all_ensembles():
    with db_helper.session_maker() as session:
        ensembles = session.query(Ensemble).all()
        return ensembles


@router.get('/ensembles/{id}')
def get_ensemble(id: int):
    with db_helper.session_maker() as session:
        ensemble = session.query(Ensemble).filter_by(id=id).first()
        return ensemble


@router.post('/ensembles/', status_code=201)
def add_ensemble(ensemble_data: EnsembleSchema):
    with db_helper.session_maker() as session:
        ensemble = Ensemble(
            name=ensemble_data.name,
            about=ensemble_data.about,
            ensemble_type=ensemble_data.ensemble_type,
        )
        session.add(ensemble)
        session.commit()
        return ensemble.id
    

@router.put('/ensembles/{id}')
def update_ensemble(id: int, ensemble_data: EnsembleSchema):
    with db_helper.session_maker() as session:
        ensemble = session.query(Ensemble).filter_by(id=id).first()
        for key, value in ensemble_data.model_dump().items():
            setattr(ensemble, key, value)
        session.commit()
        session.refresh(ensemble)
        return ensemble
    

@router.delete('/ensembles/{id}/')
def delete_ensemble(id: int):
    with db_helper.session_maker() as session:
        session.query(Ensemble).filter_by(id=id).delete()
        session.commit()

