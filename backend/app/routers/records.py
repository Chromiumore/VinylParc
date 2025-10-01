from fastapi import APIRouter
from ..database import db_helper
from ..models import Record
from ..schemas import RecordSchema


router = APIRouter(tags=['records'])


@router.get('/records')
def get_all_records():
    with db_helper.session_maker() as session:
        records = session.query(Record).all()
        return records
    

@router.get('/records/{id}')
def get_record(id: int):
    with db_helper.session_maker() as session:
        record = session.query(Record).filter_by(id=id).first()
        return record


@router.post('/records/', status_code=201)
def add_record(record_data: RecordSchema):
    with db_helper.session_maker() as session:
        record = Record(
            company=record_data.company,
            wholesale_company_address=record_data.wholesale_company_address,
            retail_price=record_data.retail_price,
            wholesale_price=record_data.wholesale_price,
            release_date=record_data.release_date,
            current_year_sold=record_data.current_year_sold,
            last_year_sold=record_data.last_year_sold,
            remaining_stock=record_data.remaining_stock,
        )
        session.add(record)
        session.commit()
        return record.id
    

@router.put('/records/{id}')
def update_record(id: int, record_data: RecordSchema):
    with db_helper.session_maker() as session:
        record = session.query(Record).filter_by(id=id).first()
        for key, value in record_data.model_dump().items():
            setattr(record, key, value)
        session.commit()
        session.refresh(record)
        return record
    

@router.delete('/records/{id}/')
def delete_record(id: int):
    with db_helper.session_maker() as session:
        session.query(Record).filter_by(id=id).delete()
        session.commit()
