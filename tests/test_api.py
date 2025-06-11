import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app, db
from models import User, Coffee, Purchase
import json

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key-12345',
        'JWT_COOKIE_SECURE': False,
        'JWT_TOKEN_LOCATION': ['headers'],
        'JWT_HEADER_NAME': 'Authorization',
        'JWT_HEADER_TYPE': 'Bearer',
        'JWT_ACCESS_TOKEN_EXPIRES': False  # Tokens don't expire in tests
    }
    
    app = create_app(test_config)
    return app

@pytest.fixture(scope='function')
def _db(app):
    """Create a fresh database for each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app, _db):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def admin_user(app, _db):
    """Create an admin user for testing."""
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
    """Create a regular user for testing."""
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
    """Create a coffee item for testing."""
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
        _db.session.expunge(coffee)  # Detach the object to avoid issues
        return coffee_id

def get_auth_token(client, username, password):
    """Helper function to get authentication token."""
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
    # Verify token format
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0

def test_add_coffee_admin(client, admin_user, _db):
    # Get admin token
    token = get_auth_token(client, 'admin', 'admin123')
    
    # Add coffee
    response = client.post('/coffee',
        json={
            'name': 'New Coffee',
            'description': 'New Description',
            'price': 15.0,
            'stock': 50
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Debug: Print response if not 201
    if response.status_code != 201:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        print(f"Token: {token[:50]}...")  # Print first 50 chars of token
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Coffee'
    assert data['price'] == 15.0

def test_add_coffee_regular_user(client, regular_user, _db):
    # Get regular user token
    token = get_auth_token(client, 'user', 'user123')
    
    # Try to add coffee
    response = client.post('/coffee',
        json={
            'name': 'New Coffee',
            'description': 'New Description',
            'price': 15.0,
            'stock': 50
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Debug: Print response if not 403
    if response.status_code != 403:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == 403

def test_purchase_coffee(client, regular_user, coffee_item, _db):
    # Get regular user token
    token = get_auth_token(client, 'user', 'user123')
    
    # Make purchase
    response = client.post('/purchase',
        json={
            'coffee_id': coffee_item,
            'quantity': 2
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Debug: Print response if not 201
    if response.status_code != 201:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['quantity'] == 2
    assert data['total_price'] == 20.0  # 2 * 10.0 (price)
    
    # Check if stock was updated
    updated_coffee = Coffee.query.get(coffee_item)
    assert updated_coffee.stock == 98

def test_get_purchase_history(client, regular_user, coffee_item, _db):
    # Get regular user token
    token = get_auth_token(client, 'user', 'user123')
    
    # Make a purchase
    purchase_response = client.post('/purchase',
        json={
            'coffee_id': coffee_item,
            'quantity': 1
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert purchase_response.status_code == 201
    
    # Get purchase history
    response = client.get('/purchase',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Debug: Print response if not 200
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == 200
    purchases = json.loads(response.data)
    assert len(purchases) == 1
    assert purchases[0]['quantity'] == 1
    assert purchases[0]['total_price'] == 10.0  # 1 * 10.0 (price) 