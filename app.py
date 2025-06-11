from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

# Initialize extensions without app
load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///coffee_shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json'
    
    # JWT Configuration
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Override config with test config if provided
    if test_config:
        app.config.update(test_config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error": "Authorization token is required"}), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Fresh token required"}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has been revoked"}), 401
    
    # Import models and blueprints
    from models import User, Coffee, Purchase
    from routes import auth_bp, coffee_bp, purchase_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(coffee_bp, url_prefix='/coffee')
    app.register_blueprint(purchase_bp, url_prefix='/purchase')
    
    return app

# Create the app instance for deployment
app = create_app()

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)