import os
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env nếu có
load_dotenv()

class Config:
    # Cấu hình cơ sở dữ liệu MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:1111@localhost/my_healthcare_app')
    
    # Vô hiệu hóa cảnh báo theo dõi các thay đổi trong mô hình (không cần thiết)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # # Secret key dùng cho việc mã hóa, bảo mật sessions, tokens
    # SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    
    # # Cấu hình cho các yếu tố khác, ví dụ như email, redis...
    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    # MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@yourapp.com')

