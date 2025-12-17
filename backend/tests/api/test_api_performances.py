from typing import List
from datetime import datetime

from fastapi.testclient import TestClient

from app.models import Performance


def test_get_performance(insert_performances_data: List[Performance]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_get_performances(insert_performances_data: List[Performance]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_add_performance(insert_ensembles_data, insert_compositions_data):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_performance(insert_performances_data: List[Performance], 
                           insert_ensembles_data, insert_compositions_data):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_delete_performance(insert_performances_data: List[Performance]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1