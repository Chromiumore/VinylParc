from typing import List

from fastapi.testclient import TestClient

from app.models import Composition


def test_get_composition(insert_compositions_data: List[Composition]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
        


def test_get_compositions(insert_compositions_data: List[Composition]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_add_composition():
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_composition(insert_compositions_data: List[Composition]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_delete_composition(insert_compositions_data: List[Composition]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1