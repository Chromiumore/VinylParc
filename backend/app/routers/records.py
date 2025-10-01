from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from authx import RequestToken
from ..database import db_helper
from ..models import Record, Performance
from ..schemas import RecordSchema, RecordResponse
from ..auth import auth


router = APIRouter(tags=['records'])


@router.get('/records', response_model=List[RecordResponse])
def get_all_records():
    with db_helper.session_maker() as session:
        records = session.query(Record).options(selectinload(Record.performances)).all()
        return records
    

@router.get('/records/{id}', response_model=RecordResponse)
def get_record(id: int):
    with db_helper.session_maker() as session:
        record = session.query(Record).options(selectinload(Record.performances)).filter_by(id=id).first()
        return record


@router.post('/records/', status_code=201, dependencies=[Depends(auth.get_token_from_request)])
def add_record(record_data: RecordSchema, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        performances = session.query(Performance).filter(Performance.id.in_(record_data.performances_id)).all()
        record = Record(
            company=record_data.company,
            wholesale_company_address=record_data.wholesale_company_address,
            retail_price=record_data.retail_price,
            wholesale_price=record_data.wholesale_price,
            release_date=record_data.release_date,
            current_year_sold=record_data.current_year_sold,
            last_year_sold=record_data.last_year_sold,
            remaining_stock=record_data.remaining_stock,
            performances=performances
        )
        session.add(record)
        session.commit()
        return record.id
    

@router.put('/records/{id}', response_model=RecordResponse, dependencies=[Depends(auth.get_token_from_request)])
def update_record(id: int, record_data: RecordSchema, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        performances = session.query(Performance).filter(Performance.id.in_(record_data.performances_id)).all()
        record = session.query(Record).options(selectinload(Record.performances)).filter_by(id=id).first()
        for key, value in record_data.model_dump().items():
            if key != 'performances_id': setattr(record, key, value)
        record.performances = performances
        session.commit()
        session.refresh(record)
        return record
    

@router.delete('/records/{id}/', dependencies=[Depends(auth.get_token_from_request)])
def delete_record(id: int, token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
    with db_helper.session_maker() as session:
        session.query(Record).filter_by(id=id).delete()
        session.commit()
