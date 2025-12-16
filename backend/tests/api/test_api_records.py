from typing import List
from datetime import datetime

from fastapi.testclient import TestClient

from app.models import Record


def test_get_record(client: TestClient, insert_records_data: List[Record]):
    for record in insert_records_data:
        id = record.id
        response = client.get(f'/records/{id}')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert data['id'] == record.id
        assert data['company'] == record.company
        assert data['wholesale_company_address'] == record.wholesale_company_address
        assert float(data['retail_price']) == float(record.retail_price)
        assert float(data['wholesale_price']) == float(record.wholesale_price)
        assert datetime.strptime(data['release_date'], '%Y-%m-%d').date() == record.release_date
        assert data['current_year_sold'] == record.current_year_sold
        assert data['last_year_sold'] == record.last_year_sold
        assert data['remaining_stock'] == record.remaining_stock
        assert len(data['performances']) == len(record.performances)


def test_get_records(client: TestClient, insert_records_data: List[Record]):
    response = client.get('/records')
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    for i in range(len(insert_records_data)):
        assert data[i]['id'] is not None
        assert data[i]['company'] == insert_records_data[i].company
        assert data[i]['wholesale_company_address'] == insert_records_data[i].wholesale_company_address
        assert float(data[i]['retail_price']) == float(insert_records_data[i].retail_price)
        assert len(data[i]['performances']) == len(insert_records_data[i].performances)


def test_add_record(client: TestClient, insert_performances_data):
    test_data = {
        'company': 'New Record Company',
        'wholesale_company_address': '789 Test Ave, Chicago',
        'retail_price': 29.99,
        'wholesale_price': 18.50,
        'release_date': '2024-03-01',
        'current_year_sold': 1000,
        'last_year_sold': 0,
        'remaining_stock': 500,
        'performances_id': [p.id for p in insert_performances_data]
    }
    
    response = client.post(
        '/records/',
        json=test_data
    )
    id = response.json()
    
    assert response.status_code == 201
    assert isinstance(id, int)

    get_response = client.get(f'/records/{id}')
    assert id == get_response.json()['id']


def test_update_record(client: TestClient, insert_records_data: List[Record], insert_performances_data):
    record_old = insert_records_data[0]
    test_data = {
        'company': 'Updated Music Corp',
        'wholesale_company_address': '999 Update St, Miami',
        'retail_price': 39.99,
        'wholesale_price': 25.00,
        'release_date': '2024-04-01',
        'current_year_sold': 1500,
        'last_year_sold': 2000,
        'remaining_stock': 300,
        'performances_id': [insert_performances_data[0].id]  # Используем только один performance
    }

    response = client.put(
        f'/records/{record_old.id}',
        json=test_data
    )
    data = response.json()
    
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == record_old.id
    assert data['company'] == test_data['company']
    assert data['wholesale_company_address'] == test_data['wholesale_company_address']
    assert float(data['retail_price']) == float(test_data['retail_price'])
    assert data['current_year_sold'] == test_data['current_year_sold']
    assert len(data['performances']) == len(test_data['performances_id'])


def test_delete_record(client: TestClient, insert_records_data: List[Record]):
    for record in insert_records_data:
        response = client.delete(f'/records/{record.id}/')
        assert response.status_code == 200
        