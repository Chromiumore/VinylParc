from typing import List
from fastapi import APIRouter, Depends, HTTPException
from authx import RequestToken
from sqlalchemy.orm import selectinload
from ..database import db_helper
from ..models import Ensemble, Musician
from ..schemas import EnsembleSchema, EnsembleResponse
from ..auth import auth


router = APIRouter(tags=['ensembles'])


@router.get('/ensembles', response_model=List[EnsembleResponse])
def get_all_ensembles():
    with db_helper.session_maker() as session:
        ensembles = session.query(Ensemble).options(selectinload(Ensemble.musicians)).all()
        return ensembles


@router.get('/ensembles/{id}', response_model=EnsembleResponse)
def get_ensemble(id: int):
    with db_helper.session_maker() as session:
        ensemble = session.query(Ensemble).options(selectinload(Ensemble.musicians)).filter_by(id=id).first()
        return ensemble


@router.post('/ensembles/', status_code=201, dependencies=[Depends(auth.get_token_from_request)])
def add_ensemble(ensemble_data: EnsembleSchema, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        musicians = session.query(Musician).filter(Musician.id.in_(ensemble_data.musicians_id)).all()
        ensemble = Ensemble(
            name=ensemble_data.name,
            about=ensemble_data.about,
            ensemble_type=ensemble_data.ensemble_type,
            musicians=musicians,
        )
        session.add(ensemble)
        session.commit()
        return ensemble.id
    

@router.put('/ensembles/{id}', response_model=EnsembleResponse, dependencies=[Depends(auth.get_token_from_request)])
def update_ensemble(id: int, ensemble_data: EnsembleSchema, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        musicians = session.query(Musician).filter(Musician.id.in_(ensemble_data.musicians_id)).all()
        ensemble = session.query(Ensemble).options(selectinload(Ensemble.musicians)).filter_by(id=id).first()
        for key, value in ensemble_data.model_dump().items():
            if key != 'musicians_id': setattr(ensemble, key, value)
        ensemble.musicians = musicians
        session.commit()
        session.refresh(ensemble)
        return ensemble
    

@router.delete('/ensembles/{id}/', dependencies=[Depends(auth.get_token_from_request)])
def delete_ensemble(id: int, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        session.query(Ensemble).filter_by(id=id).delete()
        session.commit()

