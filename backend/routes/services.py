from flask import Blueprint, request, jsonify
from models import *
from utils import token_required

# Tạo Blueprint cho các route liên quan đến Medical Services
bp = Blueprint('services', __name__)

# API để lấy danh sách tất cả các dịch vụ khám chữa bệnh
@bp.route('/services', methods=['GET'])
def get_all_services():
    services = MedicalService.query.all()

    # Chuyển đổi kết quả thành JSON
    services_list = [{
        "service_id": service.service_id,
        "service_name": service.service_name,
        "description": service.description,
        "price": float(service.price)
    } for service in services]

    return jsonify(services_list), 200

# API để lấy thông tin chi tiết về một dịch vụ dựa trên service_id
@bp.route('/services/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    service = MedicalService.query.get(service_id)

    if not service:
        return jsonify({"message": "Service not found"}), 404

    service_info = {
        "service_id": service.service_id,
        "service_name": service.service_name,
        "description": service.description,
        "price": float(service.price)
    }

    return jsonify(service_info), 200

# API để đăng ký một dịch vụ khám chữa bệnh cho bệnh nhân
@bp.route('/services/register', methods=['POST'])
@token_required
def register_service():
    data = request.get_json()

    patient_id = data.get('patient_id')
    service_id = data.get('service_id')

    if not patient_id or not service_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra xem bệnh nhân và dịch vụ có tồn tại không
    patient = Patient.query.get(patient_id)
    service = MedicalService.query.get(service_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    if not service:
        return jsonify({"message": "Service not found"}), 404

    # Kiểm tra xem bệnh nhân đã đăng ký dịch vụ này chưa
    existing_registration = PatientService.query.filter_by(patient_id=patient_id, service_id=service_id).first()
    if existing_registration:
        return jsonify({"message": "Service already registered for this patient"}), 400

    # Đăng ký dịch vụ cho bệnh nhân
    new_registration = PatientService(
        patient_id=patient_id,
        service_id=service_id,
        status='Pending'  # Trạng thái ban đầu là Pending
    )

    db.session.add(new_registration)
    db.session.commit()

    return jsonify({"message": "Service registered successfully"}), 201

# API để lấy danh sách các dịch vụ mà một bệnh nhân đã đăng ký
@bp.route('/services/patient/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_services(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Lấy danh sách các dịch vụ mà bệnh nhân đã đăng ký
    services = PatientService.query.filter_by(patient_id=patient_id).all()

    # Chuyển đổi kết quả thành JSON
    services_list = [{
        "service_id": service.service_id,
        "service_name": service.service.service_name,
        "status": service.status
    } for service in services]

    return jsonify(services_list), 200

# API để cập nhật trạng thái của dịch vụ đã đăng ký
@bp.route('/services/<int:patient_service_id>', methods=['PUT'])
@token_required
def update_patient_service_status(patient_service_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status or new_status not in ['Pending', 'Completed', 'Canceled']:
        return jsonify({"message": "Invalid status. Choose from 'Pending', 'Completed', or 'Canceled'"}), 400

    # Tìm dịch vụ bệnh nhân đã đăng ký
    patient_service = PatientService.query.get(patient_service_id)

    if not patient_service:
        return jsonify({"message": "Service registration not found"}), 404

    # Cập nhật trạng thái
    patient_service.status = new_status
    db.session.commit()

    return jsonify({"message": "Service status updated successfully"}), 200
