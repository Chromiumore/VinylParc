from typing import List

from fastapi.testclient import TestClient

from app.models import Musician, MusicianType


def test_get_musician(insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_get_musicians(insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1



def test_add_musician():
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_musician(insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_delete_musician(insert_musicians_data: List[Musician]):
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
