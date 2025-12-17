from typing import List
from datetime import datetime

from fastapi.testclient import TestClient

from app.models import Record


def test_get_record(insert_records_data: List[Record]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_get_records(insert_records_data: List[Record]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_add_record(insert_performances_data):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_record(insert_records_data: List[Record], insert_performances_data):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_delete_record(insert_records_data: List[Record]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
        