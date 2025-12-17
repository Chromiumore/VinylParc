# import os
from typing import List

import pytest
from fastapi.testclient import TestClient
# from sqlalchemy import StaticPool, create_engine, Engine
from sqlalchemy.orm import Session
# from dotenv import load_dotenv, find_dotenv

from app.models import Base, Musician, MusicianType, Ensemble, EnsembleType, Composition, Record, Performance
# from app.database import db_helper
from app.main import create_app


app = create_app()


# @pytest.fixture(scope="session")
# def db_url_fixture() -> str:


#     dotenv_path = find_dotenv('.env.test', raise_error_if_not_found=True)
#     load_dotenv(dotenv_path)

#     return (f'postgresql+psycopg2://'
#             f'{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
#             )


# @pytest.fixture(scope='session')
# def engine_fixture(db_url_fixture: str):
#     engine = create_engine(
#             db_url_fixture,
#             poolclass=StaticPool
#         )
#     Base.metadata.create_all(bind=engine)
    
#     yield engine

#     Base.metadata.drop_all(bind=engine)
#     engine.dispose()


# @pytest.fixture(name='session')
# def session_fixture(engine_fixture: Engine):
#     connection = engine_fixture.connect()
#     transaction = connection.begin()
    
#     with Session(bind=connection) as session:
#         yield session
    
#     session.close()
#     transaction.rollback()
#     connection.close()


@pytest.fixture(name='session')
def session_fixture():
    yield Session()
    
    

# @pytest.fixture(name='client')
# def client_fixture(session: Session):
#     def get_session_override():
#         return session
    
#     app.dependency_overrides[db_helper.get_session] = get_session_override

#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


@pytest.fixture(name='client')
def client_fixture(session):
    client = TestClient(app)
    yield client


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
    
    # session.add_all(musicians)
    # session.commit()
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

    # session.add_all(ensembles)
    # session.commit()
    return ensembles


@pytest.fixture(name='insert_compositions_data')
def compositions_data_fixture(session: Session):
    compositions = [
        Composition(
            name='Test Rhapsody',
            about='test music is music too'
        )
    ]

    # session.add_all(compositions)
    # session.commit()
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
    
    # session.add_all(performances)
    # session.commit()
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
    
    # session.add_all(records)
    # session.commit()
    return records
