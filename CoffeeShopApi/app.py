from flask import Flask, jsonify
from datetime import timedelta
import os
from dotenv import load_dotenv

from extensions import db, jwt
from swagger_config import configure_swagger

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///coffee_shop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json'
    
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    if test_config:
        app.config.update(test_config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    api = configure_swagger(app)
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
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Coffee Shop API",
            "version": "1.0",
            "status": "✅ Funcionando!",
            "documentation": {
                "description": "API REST para gerenciar uma cafeteria",
                "authentication": "JWT Bearer Token",
                "swagger_ui_local": "/docs/",
                "swagger_ui_online": "https://flask-api-cli.onrender.com/docs/",
                "admin_credentials": {
                    "username": "admin",
                    "password": "admin123"
                }
            },
            "endpoints": {
                "auth": {
                    "register": {
                        "method": "POST",
                        "url": "/auth/register",
                        "description": "Registrar novo usuário",
                        "body": {
                            "username": "string",
                            "email": "string", 
                            "password": "string"
                        }
                    },
                    "login": {
                        "method": "POST", 
                        "url": "/auth/login",
                        "description": "Fazer login e receber token JWT",
                        "body": {
                            "username": "string",
                            "password": "string"
                        }
                    }
                },
                "coffee": {
                    "list": {
                        "method": "GET",
                        "url": "/coffee/",
                        "description": "Listar todos os cafés disponíveis"
                    },
                    "add": {
                        "method": "POST",
                        "url": "/coffee/",
                        "description": "Adicionar novo café (apenas admin)",
                        "headers": {"Authorization": "Bearer TOKEN"},
                        "body": {
                            "name": "string",
                            "description": "string",
                            "price": "number",
                            "stock": "number"
                        }
                    }
                },
                "purchase": {
                    "buy": {
                        "method": "POST",
                        "url": "/purchase/",
                        "description": "Realizar uma compra",
                        "headers": {"Authorization": "Bearer TOKEN"},
                        "body": {
                            "coffee_id": "number",
                            "quantity": "number"
                        }
                    },
                    "history": {
                        "method": "GET",
                        "url": "/purchase/",
                        "description": "Histórico de compras do usuário",
                        "headers": {"Authorization": "Bearer TOKEN"}
                    }
                }
            },
            "usage_examples": {
                "1_register": "curl -X POST http://localhost:5001/auth/register -H 'Content-Type: application/json' -d '{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"123\"}'",
                "2_login": "curl -X POST http://localhost:5001/auth/login -H 'Content-Type: application/json' -d '{\"username\":\"admin\",\"password\":\"admin123\"}'",
                "3_list_coffees": "curl http://localhost:5001/coffee/",
                "4_add_coffee": "curl -X POST http://localhost:5001/coffee/ -H 'Authorization: Bearer YOUR_TOKEN' -H 'Content-Type: application/json' -d '{\"name\":\"Espresso\",\"description\":\"Strong coffee\",\"price\":3.50,\"stock\":100}'",
                "5_buy_coffee": "curl -X POST http://localhost:5001/purchase/ -H 'Authorization: Bearer YOUR_TOKEN' -H 'Content-Type: application/json' -d '{\"coffee_id\":1,\"quantity\":2}'"
            }
        })
        
    return app

app = create_app()

with app.app_context():
    try:
        from models import User, Coffee, Purchase
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@coffee.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    except Exception as e:
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        try:
            from models import User, Coffee, Purchase
            db.create_all()
            
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin', email='admin@coffee.com', is_admin=True)
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("👤 Admin user created: admin/admin123")
            else:
                print("👤 Admin user already exists")
                
            print("✅ Database initialized!")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            db.create_all()
    
    print("\n🚀 Coffee Shop API iniciada!")
    print("🏠 Página inicial: http://localhost:5001/")
    print("📖 Documentação completa em: http://localhost:5001/")
    print("🔧 Endpoints funcionais em: /auth/, /coffee/, /purchase/")
    print("👤 Admin: admin/admin123")
    
    app.run(debug=True, port=5001)