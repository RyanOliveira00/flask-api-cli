# Coffee Shop API

A RESTful API for a coffee shop built with Flask, featuring authentication, CRUD operations, and Swagger documentation.

## Features

- User authentication with JWT
- CRUD operations for coffee products
- Purchase system with stock management
- Swagger documentation
- Unit tests with pytest
- CI/CD pipeline with GitHub Actions

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DATABASE_URL=sqlite:///coffee_shop.db
JWT_SECRET_KEY=your-secret-key
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Once the application is running, you can access the Swagger documentation at:
`http://localhost:5000/`

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new user
- POST `/auth/login` - Login and get JWT token

### Coffee
- GET `/coffee` - List all coffee products
- POST `/coffee` - Add new coffee (admin only)
- GET `/coffee/<id>` - Get coffee details
- PUT `/coffee/<id>` - Update coffee (admin only)
- DELETE `/coffee/<id>` - Delete coffee (admin only)

### Purchase
- POST `/purchase` - Make a purchase (authenticated users)
- GET `/purchase` - Get purchase history (authenticated users)

## Running Tests

```bash
pytest -s tests/ -v
```

## CI/CD

The project includes a GitHub Actions workflow that:
1. Runs flake8 for code linting
2. Executes pytest for unit testing

The workflow runs automatically on push to main and on pull requests. 