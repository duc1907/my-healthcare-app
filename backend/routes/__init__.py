from .appointment import bp as appointment_bp
from .services import bp as services_bp
from .insurance import bp as insurance_bp
from .prescription import bp as prescription_bp
from .payment import bp as payment_bp
from .auth import bp as auth_bp

# Trong __init__.py, chúng ta chỉ đơn giản import tất cả các blueprint từ các tệp khác,
# rồi sử dụng chúng để đăng ký trong app.py.
