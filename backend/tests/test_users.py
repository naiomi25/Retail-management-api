def test_user_registration_success(client):
    
    # Prueba el registro exitoso de un usuario.
    
    user_data = {
        "name": "Test User",       
        "user_name": "testuser",      
        "email": "test@example.com",
        "password": "testpass123"
    }

    response = client.post(
        '/api/users/register',
        json=user_data 
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert 'message' in response_data
    print(f"✅ Usuario registrado: {response_data}")


def test_user_login_success(client, authenticated_client):
    
    # Prueba el login de un usuario ya registrado y autenticado por el fixture.
    
   
    client, _ = authenticated_client

    response = client.post(
        '/api/users/login',
        json={
            "email": "fixture@example.com",
            "password": "fixturepass"
        }
    )
    response_data = response.get_json()
    assert 'access_token' in response_data
    print(f"✅ Login exitoso!")


def test_user_registration_missing_data(client):
    
    # Prueba que el registro falle si faltan datos.
    
    incomplete_data = {"name": "Test User"}

    response = client.post(
        '/api/users/register',
        json=incomplete_data
    )

    assert response.status_code == 400
    response_data = response.get_json()
    assert 'error' in response_data
    print("✅ Rechaza correctamente datos incompletos")


def test_user_registration_email_conflict(client):
    
    # Prueba que el registro falle si el email ya existe.
    
    user_data = {
        "name": "Test User",
        "user_name": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

    # Registrar el usuario una vez
    client.post('/api/users/register', json=user_data)

    # Intentar registrarlo de nuevo
    response = client.post('/api/users/register', json=user_data)

    assert response.status_code == 409
    response_data = response.get_json()
    assert 'error' in response_data
    assert 'Usuario ya existe' in response_data['error']
    print("✅ Rechaza correctamente emails duplicados")
