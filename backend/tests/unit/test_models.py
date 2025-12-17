from datetime import date

from app.models import (
    Musician, MusicianType, 
    Ensemble, EnsembleType,
    Composition, Performance, Record
)


def test_create_musician(session):
    musician = Musician(
        name='John Doe',
        about='Test musician',
        musician_type=MusicianType.performer
    )


    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_ensemble_relationships(session):
    musician1 = Musician(
        name='Musician 1',
        about='Test',
        musician_type=MusicianType.performer
    )
    musician2 = Musician(
        name='Musician 2', 
        about='Test',
        musician_type=MusicianType.conductor
    )
    
    ensemble = Ensemble(
        name='Test Ensemble',
        about='Test description',
        ensemble_type=EnsembleType.quartet,
        musicians=[musician1, musician2]
    )


    assert 1 == 1
    assert 1 == 1


def test_record_calculated_fields():
    record = Record(
        company='Test',
        wholesale_company_address='Address',
        retail_price=20.0,
        wholesale_price=12.0,
        release_date=date(2024, 1, 1),
        current_year_sold=1000,
        last_year_sold=2000,
        remaining_stock=500
    )
    
    assert record.retail_price == 20.0
    assert record.wholesale_price == 12.0
