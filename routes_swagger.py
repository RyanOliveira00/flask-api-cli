from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from extensions import db
from models import User, Coffee, Purchase
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create namespaces for organizing endpoints
auth_ns = Namespace('auth', description='Operações de autenticação')
coffee_ns = Namespace('coffee', description='Operações com cafés')
purchase_ns = Namespace('purchase', description='Operações de compra')

# Models for documentation
user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário'),
    'is_admin': fields.Boolean(description='Se o usuário é admin (opcional, padrão: false)')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

coffee_model = coffee_ns.model('Coffee', {
    'name': fields.String(required=True, description='Nome do café'),
    'description': fields.String(required=True, description='Descrição do café'),
    'price': fields.Float(required=True, description='Preço do café'),
    'stock': fields.Integer(required=True, description='Quantidade em estoque')
})

coffee_response_model = coffee_ns.model('CoffeeResponse', {
    'id': fields.Integer(description='ID do café'),
    'name': fields.String(description='Nome do café'),
    'description': fields.String(description='Descrição do café'),
    'price': fields.Float(description='Preço do café'),
    'stock': fields.Integer(description='Quantidade em estoque')
})

purchase_model = purchase_ns.model('Purchase', {
    'coffee_id': fields.Integer(required=True, description='ID do café'),
    'quantity': fields.Integer(required=True, description='Quantidade a comprar')
})

purchase_response_model = purchase_ns.model('PurchaseResponse', {
    'id': fields.Integer(description='ID da compra'),
    'user_id': fields.Integer(description='ID do usuário'),
    'coffee_id': fields.Integer(description='ID do café'),
    'coffee_name': fields.String(description='Nome do café'),
    'quantity': fields.Integer(description='Quantidade comprada'),
    'total_price': fields.Float(description='Preço total'),
    'purchase_date': fields.String(description='Data da compra')
})

token_response_model = auth_ns.model('TokenResponse', {
    'access_token': fields.String(description='Token JWT de acesso')
})

error_model = auth_ns.model('Error', {
    'error': fields.String(description='Mensagem de erro')
})

success_model = auth_ns.model('Success', {
    'message': fields.String(description='Mensagem de sucesso')
})

# Authentication routes
@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('register_user')
    @auth_ns.expect(user_model)
    @auth_ns.response(201, 'Usuário registrado com sucesso', success_model)
    @auth_ns.response(400, 'Dados inválidos ou usuário já existe', error_model)
    @auth_ns.response(500, 'Erro interno do servidor', error_model)
    def post(self):
        """Registrar um novo usuário"""
        logger.info("Received register request")
        if not request.is_json:
            logger.error("Request is not JSON")
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()
        logger.info(f"Received registration data: {data}")
        
        if not all(k in data for k in ('username', 'email', 'password')):
            return {"error": "Missing required fields"}, 400
        
        if User.query.filter_by(username=data['username']).first():
            return {"error": "Username already exists"}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already exists"}, 400
        
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                is_admin=data.get('is_admin', False)
            )
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('login_user')
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login realizado com sucesso', token_response_model)
    @auth_ns.response(400, 'Dados inválidos', error_model)
    @auth_ns.response(401, 'Credenciais inválidas', error_model)
    def post(self):
        """Fazer login e obter token JWT"""
        logger.info("Received login request")
        if not request.is_json:
            logger.error("Request is not JSON")
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()
        logger.info(f"Received login data: {data}")
        
        if not all(k in data for k in ('username', 'password')):
            return {"error": "Missing username or password"}, 400
        
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        
        return {"error": "Invalid username or password"}, 401

# Coffee routes
@coffee_ns.route('/')
class CoffeeList(Resource):
    @coffee_ns.doc('list_coffees')
    @coffee_ns.response(200, 'Lista de cafés disponíveis', [coffee_response_model])
    def get(self):
        """Listar todos os cafés disponíveis"""
        logger.info("Received get coffees request")
        coffees = Coffee.query.all()
        return [{
            'id': coffee.id,
            'name': coffee.name,
            'description': coffee.description,
            'price': coffee.price,
            'stock': coffee.stock
        } for coffee in coffees], 200

    @coffee_ns.doc('add_coffee')
    @coffee_ns.expect(coffee_model)
    @coffee_ns.response(201, 'Café adicionado com sucesso', coffee_response_model)
    @coffee_ns.response(400, 'Dados inválidos', error_model)
    @coffee_ns.response(403, 'Acesso negado - apenas admins', error_model)
    @coffee_ns.response(500, 'Erro interno do servidor', error_model)
    @jwt_required()
    def post(self):
        """Adicionar um novo café (apenas administradores)"""
        logger.info("Received add coffee request")
        if not request.is_json:
            logger.error("Request is not JSON")
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()
        logger.info(f"Received coffee data: {data}")
        
        if not all(k in data for k in ('name', 'description', 'price', 'stock')):
            return {"error": "Missing required fields"}, 400
        
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return {"error": "Unauthorized"}, 403
        
        try:
            coffee = Coffee(
                name=data['name'],
                description=data['description'],
                price=float(data['price']),
                stock=int(data['stock'])
            )
            db.session.add(coffee)
            db.session.commit()
            return {
                'id': coffee.id,
                'name': coffee.name,
                'description': coffee.description,
                'price': coffee.price,
                'stock': coffee.stock
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

@coffee_ns.route('/<int:coffee_id>')
class CoffeeDetail(Resource):
    @coffee_ns.doc('update_coffee')
    @coffee_ns.expect(coffee_model)
    @coffee_ns.response(200, 'Café atualizado com sucesso', coffee_response_model)
    @coffee_ns.response(400, 'Dados inválidos', error_model)
    @coffee_ns.response(403, 'Acesso negado - apenas admins', error_model)
    @coffee_ns.response(404, 'Café não encontrado', error_model)
    @coffee_ns.response(500, 'Erro interno do servidor', error_model)
    @jwt_required()
    def put(self, coffee_id):
        """Atualizar um café existente (apenas administradores)"""
        logger.info(f"Received update coffee request for ID: {coffee_id}")
        if not request.is_json:
            logger.error("Request is not JSON")
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()
        logger.info(f"Received update data for coffee {coffee_id}: {data}")
        
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return {"error": "Unauthorized"}, 403
        
        coffee = Coffee.query.get_or_404(coffee_id)
        
        try:
            if 'name' in data:
                coffee.name = data['name']
            if 'description' in data:
                coffee.description = data['description']
            if 'price' in data:
                coffee.price = float(data['price'])
            if 'stock' in data:
                coffee.stock = int(data['stock'])
            
            db.session.commit()
            return {
                'id': coffee.id,
                'name': coffee.name,
                'description': coffee.description,
                'price': coffee.price,
                'stock': coffee.stock
            }, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @coffee_ns.doc('delete_coffee')
    @coffee_ns.response(200, 'Café deletado com sucesso', success_model)
    @coffee_ns.response(403, 'Acesso negado - apenas admins', error_model)
    @coffee_ns.response(404, 'Café não encontrado', error_model)
    @coffee_ns.response(500, 'Erro interno do servidor', error_model)
    @jwt_required()
    def delete(self, coffee_id):
        """Deletar um café (apenas administradores)"""
        logger.info(f"Received delete coffee request for ID: {coffee_id}")
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return {"error": "Only admins can delete coffee"}, 403
        
        coffee = Coffee.query.get_or_404(coffee_id)
        
        try:
            db.session.delete(coffee)
            db.session.commit()
            return {"message": "Coffee deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

# Purchase routes
@purchase_ns.route('/')
class PurchaseList(Resource):
    @purchase_ns.doc('create_purchase')
    @purchase_ns.expect(purchase_model)
    @purchase_ns.response(201, 'Compra realizada com sucesso', purchase_response_model)
    @purchase_ns.response(400, 'Dados inválidos ou estoque insuficiente', error_model)
    @purchase_ns.response(404, 'Café não encontrado', error_model)
    @purchase_ns.response(500, 'Erro interno do servidor', error_model)
    @jwt_required()
    def post(self):
        """Realizar uma compra"""
        logger.info("Received create purchase request")
        if not request.is_json:
            logger.error("Request is not JSON")
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()
        logger.info(f"Received purchase data: {data}")
        
        if not all(k in data for k in ('coffee_id', 'quantity')):
            return {"error": "Missing required fields"}, 400
        
        current_user_id = int(get_jwt_identity())
        coffee = Coffee.query.get_or_404(data['coffee_id'])
        
        if coffee.stock < data['quantity']:
            return {"error": "Not enough stock available"}, 400
        
        try:
            total_price = coffee.price * data['quantity']
            
            purchase = Purchase(
                user_id=current_user_id,
                coffee_id=coffee.id,
                quantity=data['quantity'],
                total_price=total_price
            )
            
            coffee.stock -= data['quantity']
            db.session.add(purchase)
            db.session.commit()
            
            return {
                'id': purchase.id,
                'user_id': purchase.user_id,
                'coffee_id': purchase.coffee_id,
                'quantity': purchase.quantity,
                'total_price': purchase.total_price,
                'purchase_date': purchase.created_at.isoformat()
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @purchase_ns.doc('get_purchase_history')
    @purchase_ns.response(200, 'Histórico de compras do usuário', [purchase_response_model])
    @jwt_required()
    def get(self):
        """Obter histórico de compras do usuário logado"""
        logger.info("Received get purchase history request")
        current_user_id = int(get_jwt_identity())
        purchases = Purchase.query.filter_by(user_id=current_user_id).all()
        
        return [{
            'id': purchase.id,
            'coffee_id': purchase.coffee_id,
            'coffee_name': purchase.coffee.name,
            'quantity': purchase.quantity,
            'total_price': purchase.total_price,
            'purchase_date': purchase.created_at.isoformat()
        } for purchase in purchases], 200 