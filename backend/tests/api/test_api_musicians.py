from typing import List

from fastapi.testclient import TestClient

from app.models import Musician, MusicianType


def test_get_musician(client: TestClient, insert_musicians_data: List[Musician]):
    for musician in insert_musicians_data:
        id = musician.id
        response = client.get(f'/musicians/{id}')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert data['id'] == musician.id
        assert data['name'] == musician.name
        assert data['about'] == musician.about
        assert data['musician_type'] == musician.musician_type.value


def test_get_musicians(client: TestClient, insert_musicians_data: List[Musician]):
    response = client.get('/musicians')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    for i in range(len(insert_musicians_data)):
        assert data[i]['id'] is not None
        assert data[i]['name'] == insert_musicians_data[i].name
        assert data[i]['about'] == insert_musicians_data[i].about
        assert data[i]['musician_type'] == insert_musicians_data[i].musician_type.value



def test_add_musician(client: TestClient):
    test_data = {'name': 'aaabbbccc', 'about': 'sosa', 'musician_type': MusicianType.conductor.value}
    
    response = client.post(
        '/musicians/',
        json=test_data
        )
    id = response.json()

    
    assert response.status_code == 201
    assert isinstance(id, int)

    get_response = client.get(f'/musicians/{id}')
    assert id == get_response.json()['id']


def test_update_musician(client: TestClient, insert_musicians_data: List[Musician]):
    musician_old = insert_musicians_data[0]
    test_data = {'name': 'updated_data123123', 'about': 'new_desc111111', 'musician_type': MusicianType.director.value}

    response = client.put(
        f'/musicians/{musician_old.id}',
        json=test_data
        )
    data = response.json()
    
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == musician_old.id
    assert data['name'] == test_data['name']
    assert data['about'] == test_data['about']
    assert data['musician_type'] == test_data['musician_type']


def test_delete_musician(client: TestClient, insert_musicians_data: List[Musician]):
    for musician in insert_musicians_data:
        response = client.delete(f'/musicians/{musician.id}/')

        assert response.status_code == 200
        
        get_response = client.get(f'/musicians/{musician.id}')
        assert get_response.json() is None
        
