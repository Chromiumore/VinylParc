from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
#from authx import RequestToken
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


@router.post('/records/', status_code=201)
def add_record(record_data: RecordSchema):
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
    

@router.put('/records/{id}', response_model=RecordResponse)
def update_record(id: int, record_data: RecordSchema):
    with db_helper.session_maker() as session:
        performances = session.query(Performance).filter(Performance.id.in_(record_data.performances_id)).all()
        record = session.query(Record).options(selectinload(Record.performances)).filter_by(id=id).first()
        for key, value in record_data.model_dump().items():
            if key != 'performances_id': setattr(record, key, value)
        record.performances = performances
        session.commit()
        session.refresh(record)
        return record
    

@router.delete('/records/{id}/')
def delete_record(id: int):
    with db_helper.session_maker() as session:
        session.query(Record).filter_by(id=id).delete()
        session.commit()



# 1. Flake8 BLOCKER: синтаксическая ошибка
if True  # E999 - Missing colon

# 2. Bandit CRITICAL: shell injection
import subprocess
subprocess.run("rm -rf /tmp/test", shell=True)  # B602

# 3. Detect-secrets: реальный AWS ключ
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
