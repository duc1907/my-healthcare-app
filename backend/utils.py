import jwt
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Secret key cho JWT
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

# Hàm mã hóa mật khẩu
def hash_password(password):
    """
    Mã hóa mật khẩu sử dụng bcrypt thông qua werkzeug.
    """
    return generate_password_hash(password)

# Hàm kiểm tra mật khẩu đã mã hóa
def check_password(hashed_password, password):
    """
    So sánh mật khẩu người dùng nhập với mật khẩu đã được mã hóa.
    """
    return check_password_hash(hashed_password, password)

# Hàm tạo JWT token
def generate_token(user_id, role, expires_in=24):
    """
    Tạo JWT token cho người dùng với thông tin user_id và role.
    Token sẽ hết hạn sau 'expires_in' giờ (mặc định là 24 giờ).
    """
    expiration = datetime.utcnow() + timedelta(hours=expires_in)
    token = jwt.encode({
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    
    return token

# Hàm kiểm tra và giải mã JWT token
def decode_token(token):
    """
    Giải mã JWT token. Nếu token không hợp lệ hoặc hết hạn, trả về None.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None  # Token đã hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ

# Hàm trả về lỗi nếu token không hợp lệ
def token_required(f):
    """
    Decorator yêu cầu token JWT hợp lệ trước khi truy cập vào route.
    """
    from functools import wraps
    from flask import request

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Lấy token từ header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # 'Bearer <token>'

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = decode_token(token)
            if not data:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Thêm thông tin người dùng vào request để sử dụng trong route
        request.user_id = data['user_id']
        request.user_role = data['role']
        
        return f(*args, **kwargs)

    return decorated

# Hàm kiểm tra quyền truy cập (dựa trên vai trò)
def role_required(required_role):
    """
    Decorator yêu cầu người dùng có vai trò phù hợp (ví dụ: Admin, Doctor) trước khi truy cập route.
    """
    from functools import wraps
    from flask import request

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user_role != required_role:
            return jsonify({'message': f'Permission denied: {required_role} role required!'}), 403
        return f(*args, **kwargs)

    return decorated
