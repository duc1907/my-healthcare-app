from flask import Blueprint, request, jsonify
from models import *
from utils import token_required

# Tạo Blueprint cho các route liên quan đến Prescriptions
bp = Blueprint('prescription', __name__)

# API để tạo mới một đơn thuốc
@bp.route('/prescriptions', methods=['POST'])
@token_required
def create_prescription():
    data = request.get_json()

    patient_id = data.get('patient_id')
    medication_id = data.get('medication_id')
    dosage = data.get('dosage')
    quantity = data.get('quantity')

    if not patient_id or not medication_id or not dosage or not quantity:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra xem bệnh nhân và thuốc có tồn tại không
    patient = Patient.query.get(patient_id)
    medication = Medication.query.get(medication_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    if not medication:
        return jsonify({"message": "Medication not found"}), 404

    # Tạo đơn thuốc mới
    new_prescription = Prescription(
        patient_id=patient_id,
        medication_id=medication_id,
        dosage=dosage,
        quantity=quantity
    )

    db.session.add(new_prescription)
    db.session.commit()

    return jsonify({"message": "Prescription created successfully"}), 201

# API để lấy danh sách các đơn thuốc của một bệnh nhân
@bp.route('/prescriptions/patient/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_prescriptions(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Lấy danh sách các đơn thuốc của bệnh nhân
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()

    # Chuyển đổi kết quả thành JSON
    prescriptions_list = [{
        "prescription_id": prescription.prescription_id,
        "medication_name": prescription.medication.medication_name,
        "dosage": prescription.dosage,
        "quantity": prescription.quantity
    } for prescription in prescriptions]

    return jsonify(prescriptions_list), 200

# API để lấy thông tin chi tiết của một đơn thuốc dựa trên prescription_id
@bp.route('/prescriptions/<int:prescription_id>', methods=['GET'])
@token_required
def get_prescription_by_id(prescription_id):
    prescription = Prescription.query.get(prescription_id)

    if not prescription:
        return jsonify({"message": "Prescription not found"}), 404

    prescription_info = {
        "prescription_id": prescription.prescription_id,
        "patient_id": prescription.patient_id,
        "patient_name": prescription.patient.name,
        "medication_id": prescription.medication_id,
        "medication_name": prescription.medication.medication_name,
        "dosage": prescription.dosage,
        "quantity": prescription.quantity
    }

    return jsonify(prescription_info), 200

# API để cập nhật một đơn thuốc
@bp.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
@token_required
def update_prescription(prescription_id):
    data = request.get_json()

    dosage = data.get('dosage')
    quantity = data.get('quantity')

    if not dosage or not quantity:
        return jsonify({"message": "Missing required fields"}), 400

    # Tìm đơn thuốc theo prescription_id
    prescription = Prescription.query.get(prescription_id)

    if not prescription:
        return jsonify({"message": "Prescription not found"}), 404

    # Cập nhật thông tin đơn thuốc
    prescription.dosage = dosage
    prescription.quantity = quantity

    db.session.commit()

    return jsonify({"message": "Prescription updated successfully"}), 200

# API để xóa một đơn thuốc
@bp.route('/prescriptions/<int:prescription_id>', methods=['DELETE'])
@token_required
def delete_prescription(prescription_id):
    # Tìm đơn thuốc theo prescription_id
    prescription = Prescription.query.get(prescription_id)

    if not prescription:
        return jsonify({"message": "Prescription not found"}), 404

    # Xóa đơn thuốc
    db.session.delete(prescription)
    db.session.commit()

    return jsonify({"message": "Prescription deleted successfully"}), 200
