from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db  # import db từ models.py
from routes import appointment, services, insurance, prescription, payment, auth

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Nạp cấu hình từ tệp config.py
app.config.from_object(Config)

# Kết nối SQLAlchemy với ứng dụng Flask
db.init_app(app)

# Tạo bảng dữ liệu nếu chưa có
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

# Kích hoạt CORS để cho phép React frontend tương tác với Flask backend
CORS(app)

# Đăng ký các Blueprint (API routes) từ thư mục routes/
app.register_blueprint(appointment.bp, url_prefix='/api')
app.register_blueprint(services.bp, url_prefix='/api')
app.register_blueprint(insurance.bp, url_prefix='/api')
app.register_blueprint(prescription.bp, url_prefix='/api')
app.register_blueprint(payment.bp, url_prefix='/api')
app.register_blueprint(auth.bp, url_prefix='/api')

# Route kiểm tra xem ứng dụng backend có hoạt động không
@app.route('/')
def index():
    return {"message": "Welcome to the Healthcare API!"}

# Điểm khởi động ứng dụng
if __name__ == '__main__':
    app.run(debug=True)
