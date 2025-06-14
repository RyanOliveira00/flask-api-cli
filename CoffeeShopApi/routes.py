from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from extensions import db
from models import User, Coffee, Purchase
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)
coffee_bp = Blueprint('coffee', __name__)
purchase_bp = Blueprint('purchase', __name__)
@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    logger.info("Received register request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    logger.info(f"Received registration data: {data}")
    
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({"error": "Missing required fields"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    logger.info("Received login request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    logger.info(f"Received login data: {data}")
    
    if not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

@coffee_bp.route('', methods=['GET'])
@coffee_bp.route('/', methods=['GET'])
def get_coffees():
    logger.info("Received get coffees request")
    coffees = Coffee.query.all()
    return jsonify([{
        'id': coffee.id,
        'name': coffee.name,
        'description': coffee.description,
        'price': coffee.price,
        'stock': coffee.stock
    } for coffee in coffees]), 200

@coffee_bp.route('', methods=['POST'])
@coffee_bp.route('/', methods=['POST'])
@jwt_required()
def add_coffee():
    logger.info("Received add coffee request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    logger.info(f"Received coffee data: {data}")
    
    if not all(k in data for k in ('name', 'description', 'price', 'stock')):
        return jsonify({"error": "Missing required fields"}), 400
    
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        coffee = Coffee(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            stock=int(data['stock'])
        )
        db.session.add(coffee)
        db.session.commit()
        return jsonify({
            'id': coffee.id,
            'name': coffee.name,
            'description': coffee.description,
            'price': coffee.price,
            'stock': coffee.stock
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@coffee_bp.route('/<int:coffee_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_coffee(coffee_id):
    logger.info(f"Received update coffee request for ID: {coffee_id}")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    logger.info(f"Received update data for coffee {coffee_id}: {data}")
    
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    
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
        return jsonify({
            'id': coffee.id,
            'name': coffee.name,
            'description': coffee.description,
            'price': coffee.price,
            'stock': coffee.stock
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@coffee_bp.route('/<int:coffee_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_coffee(coffee_id):
    logger.info(f"Received delete coffee request for ID: {coffee_id}")
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({"error": "Only admins can delete coffee"}), 403
    
    coffee = Coffee.query.get_or_404(coffee_id)
    
    try:
        db.session.delete(coffee)
        db.session.commit()
        return jsonify({"message": "Coffee deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@purchase_bp.route('', methods=['POST'])
@purchase_bp.route('/', methods=['POST'])
@jwt_required()
def create_purchase():
    logger.info("Received create purchase request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()
    logger.info(f"Received purchase data: {data}")
    
    if not all(k in data for k in ('coffee_id', 'quantity')):
        return jsonify({"error": "Missing required fields"}), 400
    
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    coffee = Coffee.query.get(data['coffee_id'])
    if not coffee:
        return jsonify({"error": "Coffee not found"}), 404
    
    quantity = int(data['quantity'])
    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400
    
    if coffee.stock < quantity:
        return jsonify({"error": "Insufficient stock"}), 400
    
    total_price = coffee.price * quantity
    
    try:
        purchase = Purchase(
            user_id=current_user_id,
            coffee_id=coffee.id,
            quantity=quantity,
            total_price=total_price
        )
        
        coffee.stock -= quantity
        
        db.session.add(purchase)
        db.session.commit()
        
        return jsonify({
            'id': purchase.id,
            'user_id': purchase.user_id,
            'coffee_id': purchase.coffee_id,
            'coffee_name': coffee.name,
            'quantity': purchase.quantity,
            'total_price': purchase.total_price,
            'purchase_date': purchase.created_at.isoformat()
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@purchase_bp.route('', methods=['GET'])
@purchase_bp.route('/', methods=['GET'])
@jwt_required()
def get_purchase_history():
    logger.info("Received get purchase history request")
    current_user_id = int(get_jwt_identity())
    
    purchases = Purchase.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([{
        'id': purchase.id,
        'user_id': purchase.user_id,
        'coffee_id': purchase.coffee_id,
        'coffee_name': purchase.coffee.name,
        'quantity': purchase.quantity,
        'total_price': purchase.total_price,
        'purchase_date': purchase.created_at.isoformat()
    } for purchase in purchases]), 200 