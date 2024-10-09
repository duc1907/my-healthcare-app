from flask import Blueprint, request, jsonify
from models import *
from utils import token_required

# Tạo Blueprint cho các route liên quan đến Insurance Services
bp = Blueprint('insurance', __name__)

# API để lấy danh sách tất cả các gói bảo hiểm
@bp.route('/insurance', methods=['GET'])
def get_all_insurance():
    insurance_services = InsuranceService.query.all()

    # Chuyển đổi kết quả thành JSON
    insurance_list = [{
        "insurance_id": insurance.insurance_id,
        "insurance_name": insurance.insurance_name,
        "coverage": insurance.coverage,
        "price": float(insurance.price)
    } for insurance in insurance_services]

    return jsonify(insurance_list), 200

# API để lấy thông tin chi tiết về một gói bảo hiểm dựa trên insurance_id
@bp.route('/insurance/<int:insurance_id>', methods=['GET'])
def get_insurance_by_id(insurance_id):
    insurance = InsuranceService.query.get(insurance_id)

    if not insurance:
        return jsonify({"message": "Insurance not found"}), 404

    insurance_info = {
        "insurance_id": insurance.insurance_id,
        "insurance_name": insurance.insurance_name,
        "coverage": insurance.coverage,
        "price": float(insurance.price)
    }

    return jsonify(insurance_info), 200

# API để đăng ký một gói bảo hiểm cho bệnh nhân
@bp.route('/insurance/register', methods=['POST'])
@token_required
def register_insurance():
    data = request.get_json()

    patient_id = data.get('patient_id')
    insurance_id = data.get('insurance_id')

    if not patient_id or not insurance_id:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra xem bệnh nhân và gói bảo hiểm có tồn tại không
    patient = Patient.query.get(patient_id)
    insurance = InsuranceService.query.get(insurance_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    if not insurance:
        return jsonify({"message": "Insurance not found"}), 404

    # Kiểm tra xem bệnh nhân đã đăng ký gói bảo hiểm này chưa
    existing_registration = PatientInsurance.query.filter_by(patient_id=patient_id, insurance_id=insurance_id).first()
    if existing_registration:
        return jsonify({"message": "Insurance already registered for this patient"}), 400

    # Đăng ký gói bảo hiểm cho bệnh nhân
    new_registration = PatientInsurance(
        patient_id=patient_id,
        insurance_id=insurance_id,
        status='Active'  # Trạng thái ban đầu là Active
    )

    db.session.add(new_registration)
    db.session.commit()

    return jsonify({"message": "Insurance registered successfully"}), 201

# API để lấy danh sách các gói bảo hiểm mà một bệnh nhân đã đăng ký
@bp.route('/insurance/patient/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_insurances(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Lấy danh sách các gói bảo hiểm mà bệnh nhân đã đăng ký
    insurances = PatientInsurance.query.filter_by(patient_id=patient_id).all()

    # Chuyển đổi kết quả thành JSON
    insurance_list = [{
        "insurance_id": insurance.insurance_id,
        "insurance_name": insurance.insurance.insurance_name,
        "status": insurance.status
    } for insurance in insurances]

    return jsonify(insurance_list), 200

# API để cập nhật trạng thái của gói bảo hiểm đã đăng ký
@bp.route('/insurance/<int:patient_insurance_id>', methods=['PUT'])
@token_required
def update_patient_insurance_status(patient_insurance_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status or new_status not in ['Active', 'Expired']:
        return jsonify({"message": "Invalid status. Choose from 'Active' or 'Expired'"}), 400

    # Tìm gói bảo hiểm bệnh nhân đã đăng ký
    patient_insurance = PatientInsurance.query.get(patient_insurance_id)

    if not patient_insurance:
        return jsonify({"message": "Insurance registration not found"}), 404

    # Cập nhật trạng thái
    patient_insurance.status = new_status
    db.session.commit()

    return jsonify({"message": "Insurance status updated successfully"}), 200
