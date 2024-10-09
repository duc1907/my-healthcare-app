from flask import Blueprint, request, jsonify
from models import *
from utils import token_required
from datetime import datetime

# Tạo Blueprint cho các route liên quan đến Payment
bp = Blueprint('payment', __name__)

# API để tạo một thanh toán mới cho bệnh nhân
@bp.route('/payments', methods=['POST'])
@token_required
def create_payment():
    data = request.get_json()

    patient_id = data.get('patient_id')
    amount = data.get('amount')
    description = data.get('description')

    if not patient_id or not amount or not description:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra xem bệnh nhân có tồn tại không
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Tạo thanh toán mới
    new_payment = Payment(
        patient_id=patient_id,
        amount=amount,
        payment_date=datetime.utcnow(),
        description=description,
        status='Paid'
    )

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "Payment made successfully"}), 201

# API để lấy danh sách các thanh toán của một bệnh nhân
@bp.route('/payments/patient/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_payments(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Lấy danh sách các thanh toán của bệnh nhân
    payments = Payment.query.filter_by(patient_id=patient_id).all()

    # Chuyển đổi kết quả thành JSON
    payments_list = [{
        "payment_id": payment.payment_id,
        "amount": float(payment.amount),
        "payment_date": payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
        "description": payment.description,
        "status": payment.status
    } for payment in payments]

    return jsonify(payments_list), 200

# API để lấy thông tin chi tiết về một thanh toán dựa trên payment_id
@bp.route('/payments/<int:payment_id>', methods=['GET'])
@token_required
def get_payment_by_id(payment_id):
    payment = Payment.query.get(payment_id)

    if not payment:
        return jsonify({"message": "Payment not found"}), 404

    payment_info = {
        "payment_id": payment.payment_id,
        "patient_id": payment.patient_id,
        "patient_name": payment.patient.name,
        "amount": float(payment.amount),
        "payment_date": payment.payment_date.strftime('%Y-%m-%d %H:%M:%S'),
        "description": payment.description,
        "status": payment.status
    }

    return jsonify(payment_info), 200

# API để cập nhật trạng thái của thanh toán (ví dụ: 'Paid', 'Pending')
@bp.route('/payments/<int:payment_id>', methods=['PUT'])
@token_required
def update_payment_status(payment_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status or new_status not in ['Paid', 'Pending']:
        return jsonify({"message": "Invalid status. Choose from 'Paid' or 'Pending'"}), 400

    # Tìm thanh toán theo payment_id
    payment = Payment.query.get(payment_id)

    if not payment:
        return jsonify({"message": "Payment not found"}), 404

    # Cập nhật trạng thái của thanh toán
    payment.status = new_status
    db.session.commit()

    return jsonify({"message": "Payment status updated successfully"}), 200

# API để xóa một thanh toán
@bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@token_required
def delete_payment(payment_id):
    # Tìm thanh toán theo payment_id
    payment = Payment.query.get(payment_id)

    if not payment:
        return jsonify({"message": "Payment not found"}), 404

    # Xóa thanh toán
    db.session.delete(payment)
    db.session.commit()

    return jsonify({"message": "Payment deleted successfully"}), 200
