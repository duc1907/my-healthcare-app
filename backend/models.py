from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Định nghĩa bảng Patient
class Patient(db.Model):
    __tablename__ = 'Patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)  # Date of Birth
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    medical_history = db.Column(db.Text, nullable=True)

    # Quan hệ với Appointment
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    # Quan hệ với PatientService
    services = db.relationship('PatientService', backref='patient', lazy=True)
    # Quan hệ với PatientInsurance
    insurances = db.relationship('PatientInsurance', backref='patient', lazy=True)
    # Quan hệ với Prescription
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True)

# Định nghĩa bảng Doctor
class Doctor(db.Model):
    __tablename__ = 'Doctor'
    doctor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    # Quan hệ với Appointment
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

# Định nghĩa bảng Appointment (Lịch hẹn)
class Appointment(db.Model):
    __tablename__ = 'Appointment'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctor.doctor_id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Scheduled, Completed, Canceled

# Định nghĩa bảng MedicalService (Dịch vụ khám chữa bệnh)
class MedicalService(db.Model):
    __tablename__ = 'MedicalService'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Quan hệ với PatientService
    patients = db.relationship('PatientService', backref='service', lazy=True)

# Định nghĩa bảng PatientService (Bệnh nhân đăng ký dịch vụ)
class PatientService(db.Model):
    __tablename__ = 'PatientService'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.patient_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('MedicalService.service_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Pending, Completed

# Định nghĩa bảng InsuranceService (Gói bảo hiểm)
class InsuranceService(db.Model):
    __tablename__ = 'InsuranceService'
    insurance_id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String(255), nullable=False)
    coverage = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Quan hệ với PatientInsurance
    patients = db.relationship('PatientInsurance', backref='insurance', lazy=True)

# Định nghĩa bảng PatientInsurance (Bệnh nhân đăng ký bảo hiểm)
class PatientInsurance(db.Model):
    __tablename__ = 'PatientInsurance'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.patient_id'), nullable=False)
    insurance_id = db.Column(db.Integer, db.ForeignKey('InsuranceService.insurance_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Active, Expired

# Định nghĩa bảng Medication (Thuốc)
class Medication(db.Model):
    __tablename__ = 'Medication'
    medication_id = db.Column(db.Integer, primary_key=True)
    medication_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Quan hệ với Prescription
    prescriptions = db.relationship('Prescription', backref='medication', lazy=True)

# Định nghĩa bảng Prescription (Đơn thuốc)
class Prescription(db.Model):
    __tablename__ = 'Prescription'
    prescription_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.patient_id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('Medication.medication_id'), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Định nghĩa bảng Payment (Thanh toán)
class Payment(db.Model):
    __tablename__ = 'Payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.patient_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False)  # Paid, Pending

# Định nghĩa bảng User (Quản lý người dùng và quyền truy cập)
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Admin, Doctor, Patient

# # Định nghĩa bảng User (Quản lý người dùng và quyền truy cập)
# class UserTest(db.Model):
#     __tablename__ = 'UserTest'
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # Admin, Doctor, Patient
