from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime
from utils import token_required

# Tạo Blueprint cho các route liên quan đến Appointment
bp = Blueprint('appointment', __name__)

# API để tạo mới một lịch hẹn
@bp.route('/appointments', methods=['POST'])
@token_required
def create_appointment():
    data = request.get_json()

    # Kiểm tra các thông tin đầu vào
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    appointment_date = data.get('appointment_date')

    if not patient_id or not doctor_id or not appointment_date:
        return jsonify({"message": "Missing required fields"}), 400

    try:
        # Chuyển đổi chuỗi thành datetime
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD HH:MM"}), 400

    # Kiểm tra xem bệnh nhân và bác sĩ có tồn tại hay không
    patient = Patient.query.get(patient_id)
    doctor = Doctor.query.get(doctor_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404

    # Tạo lịch hẹn mới
    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        status='Scheduled'
    )

    # Lưu lịch hẹn vào cơ sở dữ liệu
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({"message": "Appointment scheduled successfully"}), 201

# API để lấy danh sách các lịch hẹn của một bệnh nhân
@bp.route('/appointments/patient/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_appointments(patient_id):
    patient = Patient.query.get(patient_id)

    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    # Lấy danh sách các lịch hẹn của bệnh nhân
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()

    # Chuyển đổi kết quả thành JSON
    appointments_list = [{
        "appointment_id": appt.appointment_id,
        "doctor_id": appt.doctor_id,
        "doctor_name": appt.doctor.name,
        "appointment_date": appt.appointment_date.strftime('%Y-%m-%d %H:%M'),
        "status": appt.status
    } for appt in appointments]

    return jsonify(appointments_list), 200

# API để lấy danh sách các lịch hẹn của một bác sĩ
@bp.route('/appointments/doctor/<int:doctor_id>', methods=['GET'])
@token_required
def get_doctor_appointments(doctor_id):
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return jsonify({"message": "Doctor not found"}), 404

    # Lấy danh sách các lịch hẹn của bác sĩ
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()

    # Chuyển đổi kết quả thành JSON
    appointments_list = [{
        "appointment_id": appt.appointment_id,
        "patient_id": appt.patient_id,
        "patient_name": appt.patient.name,
        "appointment_date": appt.appointment_date.strftime('%Y-%m-%d %H:%M'),
        "status": appt.status
    } for appt in appointments]

    return jsonify(appointments_list), 200

# API để cập nhật trạng thái của lịch hẹn (hoàn tất hoặc hủy)
@bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@token_required
def update_appointment_status(appointment_id):
    data = request.get_json()
    new_status = data.get('status')

    # Kiểm tra trạng thái mới
    if not new_status or new_status not in ['Scheduled', 'Completed', 'Canceled']:
        return jsonify({"message": "Invalid status. Choose from 'Scheduled', 'Completed', or 'Canceled'"}), 400

    # Tìm lịch hẹn theo appointment_id
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    # Cập nhật trạng thái của lịch hẹn
    appointment.status = new_status
    db.session.commit()

    return jsonify({"message": "Appointment status updated successfully"}), 200

# API để xóa một lịch hẹn
@bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@token_required
def delete_appointment(appointment_id):
    # Tìm lịch hẹn theo appointment_id
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    # Xóa lịch hẹn
    db.session.delete(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment deleted successfully"}), 200
