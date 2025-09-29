import json
from datetime import datetime

def test_create_and_query_entries_by_range(authenticated_client):
    """
    Test completo con cliente autenticado.
    """
    client, token = authenticated_client
    headers = {'Authorization': f'Bearer {token}'}

    entries_data = [
        {
            "date": "2024-01-15",
            "shift": "morning",
            "net_sales": 500.0,
            "transactions": 50,
            "articles": 100,
            "accessories": 30,
            "apparel": 70,
            "footfall": 80
        },
        {
            "date": "2024-01-15", 
            "shift": "evening",
            "net_sales": 800.0,
            "transactions": 60,
            "articles": 120,
            "accessories": 40,
            "apparel": 80,
            "footfall": 90
        },
        {
            "date": "2024-01-16",
            "shift": "morning", 
            "net_sales": 600.0,
            "transactions": 55,
            "articles": 110,
            "accessories": 35,
            "apparel": 75,
            "footfall": 85
        }
    ]

    
    # Crear todas las entradas
    for entry_data in entries_data:
        response = client.post(
            '/api/entries/create',
            json=entry_data,  
            headers=headers
        )
        assert response.status_code == 201
        print(f"✅ Entrada creada: {entry_data['date']} - {entry_data['shift']}")

    # Consultar por rango
    response = client.get(
        '/api/entries/range/?start_date=2024-01-15&end_date=2024-01-16',
        headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_entries'] == 3


def test_entries_with_zero_values(authenticated_client):
    client, token = authenticated_client
    headers = {'Authorization': f'Bearer {token}'}

    entry_with_zeros = {
        "date": "2024-01-16",
        "shift": "morning",
        "net_sales": 0,        
        "transactions": 0,      
        "articles": 0,        
        "accessories": 0,      
        "apparel": 0,          
        "footfall": 5
    }

    response = client.post('/api/entries/create', json=entry_with_zeros, headers=headers)
    assert response.status_code == 201
    entry_data = response.get_json()['entry']
    assert entry_data['net_sales'] == 0.0
    assert entry_data['articles'] == 0
    print("✅ Entrada con valores 0 creada correctamente")


def test_create_entry_unauthenticated(client):
    entry_data = {
        "date": datetime.strptime("2024-01-25", "%Y-%m-%d").date(),
        "shift": "morning",
        "net_sales": 100.0,
        "transactions": 10,
        "articles": 10,
        "accessories": 10,
        "apparel": 10,
        "footfall": 10
    }
    response = client.post('/api/entries/create', json=entry_data)
    assert response.status_code == 401
   
    assert "msg" in response.get_json()
    print("✅ Intento de creación sin autenticación rechazado correctamente")
