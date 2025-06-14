import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app, db
from models import User, Coffee, Purchase
import json

@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key-12345',
        'JWT_COOKIE_SECURE': False,
        'JWT_TOKEN_LOCATION': ['headers'],
        'JWT_HEADER_NAME': 'Authorization',
        'JWT_HEADER_TYPE': 'Bearer',
        'JWT_ACCESS_TOKEN_EXPIRES': False
    }
    
    app = create_app(test_config)
    return app

@pytest.fixture(scope='function')
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app, _db):
    return app.test_client()

@pytest.fixture(scope='function')
def admin_user(app, _db):
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        user.set_password('admin123')
        _db.session.add(user)
        _db.session.commit()
        return user

@pytest.fixture(scope='function')
def regular_user(app, _db):
    with app.app_context():
        user = User(
            username='user',
            email='user@example.com',
            is_admin=False
        )
        user.set_password('user123')
        _db.session.add(user)
        _db.session.commit()
        return user

@pytest.fixture(scope='function')
def coffee_item(app, _db):
    with app.app_context():
        coffee = Coffee(
            name='Test Coffee',
            description='Test Description',
            price=10.0,
            stock=100
        )
        _db.session.add(coffee)
        _db.session.commit()
        coffee_id = coffee.id
        _db.session.expunge(coffee)
        return coffee_id

def get_auth_token(client, username, password):
    response = client.post('/auth/login',
        json={
            'username': username,
            'password': password
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    return data['access_token']

def test_register_user(client):
    response = client.post('/auth/register',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
    )
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login_user(client, regular_user):
    response = client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'user123'
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0

def test_add_coffee_admin(client, admin_user, _db):
    token = get_auth_token(client, 'admin', 'admin123')
    
    response = client.post('/coffee/',
        json={
            'name': 'New Coffee',
            'description': 'New Description',
            'price': 15.0,
            'stock': 50
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 201:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        print(f"Token: {token[:50]}...")
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Coffee'
    assert data['price'] == 15.0

def test_add_coffee_regular_user(client, regular_user, _db):
    token = get_auth_token(client, 'user', 'user123')
    
    response = client.post('/coffee/',
        json={
            'name': 'New Coffee',
            'description': 'New Description',
            'price': 15.0,
            'stock': 50
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 403:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == 403

def test_purchase_coffee(client, regular_user, coffee_item, _db):
    token = get_auth_token(client, 'user', 'user123')
    
    response = client.post('/purchase/',
        json={
            'coffee_id': coffee_item,
            'quantity': 2
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 201:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['quantity'] == 2
    assert data['total_price'] == 20.0
    
    updated_coffee = Coffee.query.get(coffee_item)
    assert updated_coffee.stock == 98

def test_get_purchase_history(client, regular_user, coffee_item, _db):
    token = get_auth_token(client, 'user', 'user123')
    
    client.post('/purchase/',
        json={
            'coffee_id': coffee_item,
            'quantity': 1
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    response = client.get('/purchase/',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['quantity'] == 1

if __name__ == '__main__':
    pytest.main([__file__]) 