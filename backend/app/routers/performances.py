from fastapi import APIRouter
from ..database import db_helper
from ..models import Performance
from ..schemas import PerformanceSchema


router = APIRouter(tags=['performances'])


@router.get('/performances')
def get_all_performance():
    with db_helper.session_maker() as session:
        performances = session.query(Performance).all()
        return performances


@router.get('/performances/{id}')
def get_performance(id: int):
    with db_helper.session_maker() as session:
        performance = session.query(Performance).filter_by(id=id).first()
        return performance


@router.post('/performances/', status_code=201)
def add_performance(performance_data: PerformanceSchema):
    with db_helper.session_maker() as session:
        performance = Performance(
            performance_date=performance_data.performance_date,
            composition_id=performance_data.composition_id,
            ensemble_id=performance_data.ensemble_id,
        )
        session.add(performance)
        session.commit()
        return performance.id
    

@router.put('/performances/{id}')
def update_performance(id: int, performance_data: PerformanceSchema):
    with db_helper.session_maker() as session:
        performance = session.query(Performance).filter_by(id=id).first()
        for key, value in performance_data.model_dump().items():
            setattr(performance, key, value)
        session.commit()
        session.refresh(performance)
        return performance
    

@router.delete('/performances/{id}/')
def delete_performance(id: int):
    with db_helper.session_maker() as session:
        session.query(Performance).filter_by(id=id).delete()
        session.commit()
