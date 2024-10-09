from flask import Blueprint, request, jsonify
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate_token, token_required
import jwt
import os

# Tạo Blueprint cho các route liên quan đến Authentication
bp = Blueprint('auth', __name__)

# API để đăng ký người dùng mới (Sign up)
@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra xem người dùng đã tồn tại chưa
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Mã hóa mật khẩu và tạo người dùng mới
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# API để đăng nhập người dùng (Sign in)
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Tìm người dùng theo username
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Tạo JWT token cho người dùng
    token = generate_token(user_id=user.user_id, role=user.role)

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

# API để lấy thông tin người dùng hiện tại (Dựa trên token)
@bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    from flask import request

    user_id = request.user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }), 200

# API để kiểm tra tính hợp lệ của token (Token verification)
@bp.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"message": "Token is missing"}), 400

    try:
        decoded = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return jsonify({"message": "Token is valid", "user_id": decoded['user_id'], "role": decoded['role']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
