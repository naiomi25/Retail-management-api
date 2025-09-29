# conftest.py
import pytest
from app import create_app
from database import db

@pytest.fixture
def client():
    app = create_app("testing")
    print("\n[TESTING] Base de datos usada:", app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("[TESTING] Tablas creadas:", db.metadata.tables.keys())
        with app.test_client() as client:
            yield client

        db.session.remove()
        db.engine.dispose()

@pytest.fixture
def authenticated_client(client):
    user_data = {
        "name": "Fixture User",
        "user_name": "fixtureuser",
        "email": "fixture@example.com",
        "password": "fixturepass"
    }
    client.post('/api/users/register', json=user_data)

    login_response = client.post('/api/users/login', json={
        "email": user_data['email'],
        "password": user_data['password']
    })
    token = login_response.get_json()['access_token']

    return client, token
