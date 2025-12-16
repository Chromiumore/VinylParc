from typing import List

from fastapi.testclient import TestClient

from app.models import Composition


def test_get_composition(client: TestClient, insert_compositions_data: List[Composition]):
    for composition in insert_compositions_data:
        id = composition.id
        response = client.get(f'/compositions/{id}')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert data['id'] == composition.id
        assert data['name'] == composition.name
        assert data['about'] == composition.about


def test_get_compositions(client: TestClient, insert_compositions_data: List[Composition]):
    response = client.get('/compositions')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    for i in range(len(insert_compositions_data)):
        assert data[i]['id'] is not None
        assert data[i]['name'] == insert_compositions_data[i].name
        assert data[i]['about'] == insert_compositions_data[i].about


def test_add_composition(client: TestClient):
    test_data = {'name': 'New Test Composition', 'about': 'This is a test composition'}
    
    response = client.post(
        '/compositions/',
        json=test_data
    )
    id = response.json()
    
    assert response.status_code == 201
    assert isinstance(id, int)

    get_response = client.get(f'/compositions/{id}')
    assert id == get_response.json()['id']


def test_update_composition(client: TestClient, insert_compositions_data: List[Composition]):
    composition_old = insert_compositions_data[0]
    test_data = {'name': 'Updated Composition Name', 'about': 'Updated description'}

    response = client.put(
        f'/compositions/{composition_old.id}',
        json=test_data
    )
    data = response.json()
    
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == composition_old.id
    assert data['name'] == test_data['name']
    assert data['about'] == test_data['about']


def test_delete_composition(client: TestClient, insert_compositions_data: List[Composition]):
    for composition in insert_compositions_data:
        response = client.delete(f'/compositions/{composition.id}/')
        assert response.status_code == 200
        
        get_response = client.get(f'/compositions/{composition.id}')
        assert get_response.status_code == 200
        assert get_response.json() is None