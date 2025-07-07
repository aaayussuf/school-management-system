from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app import db, jwt
from app.models import User
from flask import Blueprint
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def auth_root():
    return jsonify({
        'message': 'Auth API root. Available endpoints: /login, /refresh, /protected'
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    if not user.is_active:
        return jsonify({'message': 'Account is disabled'}), 403

    access_token = create_access_token(
        identity={'id': user.id, 'role': user.role},
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity={'id': user.id, 'role': user.role},
        expires_delta=timedelta(days=30)
    )

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
