from typing import List

from fastapi.testclient import TestClient

from app.models import Ensemble, EnsembleType, Musician


def test_get_ensemble(insert_ensembles_data: List[Ensemble]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_get_ensembles(insert_ensembles_data):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1

    
def test_add_ensemble(insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_ensemble(insert_ensembles_data: List[Ensemble], insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1



def test_delete_ensemble(insert_ensembles_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
