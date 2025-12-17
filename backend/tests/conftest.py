from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Base, Musician, MusicianType, Ensemble, EnsembleType, Composition, Record, Performance
from app.main import create_app


app = create_app()



@pytest.fixture(name='session')
def session_fixture():
    yield Session()
    

@pytest.fixture(name='insert_musicians_data')
def musicians_data_fixture(session: Session):
    musicians = [
        Musician(
            name='Victor Testiano',
            about='Известен как Витя Самосвал',
            musician_type=MusicianType.conductor
        ),
        Musician(
            name='OG Стас',
            about='Прибаутка',
            musician_type=MusicianType.performer
        )
    ]
    
    return musicians


@pytest.fixture(name='insert_ensembles_data')
def ensembles_data_fixture(session: Session, insert_musicians_data: List[Musician]):
    ensembles = [
        Ensemble(
            name='Солнышко',
            about='Бубльгум',
            ensemble_type=EnsembleType.quartet,
            musicians=insert_musicians_data[:2],
        )
    ]

    return ensembles


@pytest.fixture(name='insert_compositions_data')
def compositions_data_fixture(session: Session):
    compositions = [
        Composition(
            name='Test Rhapsody',
            about='test music is music too'
        )
    ]

    return compositions


@pytest.fixture(name='insert_performances_data')
def performances_data_fixture(session: Session, insert_ensembles_data: List[Ensemble], insert_compositions_data: List[Composition]):
    performances = [
        Performance(
            performance_date='2024-01-15',
            composition_id=insert_compositions_data[0].id,
            ensemble_id=insert_ensembles_data[0].id,
        ),
        Performance(
            performance_date='2024-02-20',
            composition_id=insert_compositions_data[0].id,
            ensemble_id=insert_ensembles_data[0].id,
        )
    ]
    
    return performances


@pytest.fixture(name='insert_records_data')
def records_data_fixture(session: Session, insert_performances_data: List[Performance]):
    records = [
        Record(
            company='Universal Music',
            wholesale_company_address='123 Music St, LA',
            retail_price=19.99,
            wholesale_price=12.50,
            release_date='2024-01-01',
            current_year_sold=5000,
            last_year_sold=10000,
            remaining_stock=2000,
            performances=insert_performances_data[:1],
        ),
        Record(
            company='Sony Music',
            wholesale_company_address='456 Sony Ave, NY',
            retail_price=24.99,
            wholesale_price=15.00,
            release_date='2024-02-01',
            current_year_sold=3000,
            last_year_sold=8000,
            remaining_stock=1000,
            performances=insert_performances_data[1:],
        )
    ]
    
    return records
