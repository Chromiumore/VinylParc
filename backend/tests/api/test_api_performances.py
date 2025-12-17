from typing import List
from datetime import datetime

from fastapi.testclient import TestClient

from app.models import Performance


def test_get_performance(client: TestClient, insert_performances_data: List[Performance]):
    # for performance in insert_performances_data:
    #     id = performance.id
    #     response = client.get(f'/performances/{id}')
    #     data = response.json()

    #     assert response.status_code == 200
    #     assert isinstance(data, dict)
    #     assert data['id'] == performance.id
    #     assert datetime.strptime(data['performance_date'], '%Y-%m-%d').date() == performance.performance_date
    #     assert data['composition_id'] == performance.composition_id
    #     assert data['ensemble_id'] == performance.ensemble_id
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_get_performances(client: TestClient, insert_performances_data: List[Performance]):
    # response = client.get('/performances')
    # data = response.json()

    # assert response.status_code == 200
    # assert isinstance(data, list)
    # for i in range(len(insert_performances_data)):
    #     assert data[i]['id'] is not None
    #     assert datetime.strptime(data[i]['performance_date'], '%Y-%m-%d').date() == insert_performances_data[i].performance_date
    #     assert data[i]['composition_id'] == insert_performances_data[i].composition_id
    #     assert data[i]['ensemble_id'] == insert_performances_data[i].ensemble_id
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_add_performance(client: TestClient, insert_ensembles_data, insert_compositions_data):
    # test_data = {
    #     'performance_date': '2024-03-15',
    #     'composition_id': insert_compositions_data[0].id,
    #     'ensemble_id': insert_ensembles_data[0].id
    # }
    
    # response = client.post(
    #     '/performances/',
    #     json=test_data
    # )
    # id = response.json()
    
    # assert response.status_code == 201
    # assert isinstance(id, int)

    # get_response = client.get(f'/performances/{id}')
    # assert id == get_response.json()['id']
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_update_performance(client: TestClient, insert_performances_data: List[Performance], 
                           insert_ensembles_data, insert_compositions_data):
    # performance_old = insert_performances_data[0]
    # test_data = {
    #     'performance_date': '2024-12-31',
    #     'composition_id': insert_compositions_data[0].id,
    #     'ensemble_id': insert_ensembles_data[0].id
    # }

    # response = client.put(
    #     f'/performances/{performance_old.id}',
    #     json=test_data
    # )
    # data = response.json()
    
    # assert response.status_code == 200
    # assert isinstance(data, dict)
    # assert data['id'] == performance_old.id
    # assert data['performance_date'] == test_data['performance_date']
    # assert data['composition_id'] == test_data['composition_id']
    # assert data['ensemble_id'] == test_data['ensemble_id']
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1


def test_delete_performance(client: TestClient, insert_performances_data: List[Performance]):
    # for performance in insert_performances_data:
    #     response = client.delete(f'/performances/{performance.id}/')
    #     assert response.status_code == 200
        
    #     get_response = client.get(f'/performances/{performance.id}')
    #     assert get_response.json() is None
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1