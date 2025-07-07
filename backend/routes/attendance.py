from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Attendance, Student, Class
from datetime import datetime, date

attendance_bp = Blueprint('attendance_bp', __name__)

@attendance_bp.route('/', methods=['GET'])
def attendance_home():
    return jsonify({'message': 'Attendance API is working'}), 200

@attendance_bp.route('/', methods=['POST'])
@jwt_required()
def mark_attendance():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({'message': 'Expected an array of attendance records'}), 400
    
    records = []
    for record in data:
        required_fields = ['student_id', 'date', 'status']
        if not all(field in record for field in required_fields):
            continue  # Skip invalid records
        
        try:
            attendance_date = datetime.strptime(record['date'], '%Y-%m-%d').date()
        except ValueError:
            continue  # Skip records with invalid date format
        
        # Check if attendance already exists for this student on this date
        existing = Attendance.query.filter_by(
            student_id=record['student_id'],
            date=attendance_date
        ).first()
        
        if existing:
            existing.status = record['status']
            existing.remarks = record.get('remarks')
        else:
            new_attendance = Attendance(
                student_id=record['student_id'],
                date=attendance_date,
                status=record['status'],
                remarks=record.get('remarks')
            )
            db.session.add(new_attendance)
    
    db.session.commit()
    return jsonify({'message': 'Attendance recorded successfully'}), 201

@attendance_bp.route('/report', methods=['GET'])
@jwt_required()
def get_attendance_report():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    class_id = request.args.get('class_id')
    month = request.args.get('month')
    year = request.args.get('year')
    
    if not (month and year):
        return jsonify({'message': 'Month and year are required'}), 400
    
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return jsonify({'message': 'Month and year must be numbers'}), 400
    
    # Get all students in the class (if class_id is provided)
    query = Student.query.filter_by(is_active=True)
    if class_id:
        query = query.filter_by(class_id=class_id)
    students = query.all()
    
    report = []
    for student in students:
        # Get all attendance records for this student in the specified month/year
        attendances = Attendance.query.filter(
            Attendance.student_id == student.id,
            db.extract('year', Attendance.date) == year,
            db.extract('month', Attendance.date) == month
        ).all()
        
        present_days = sum(1 for a in attendances if a.status == 'present')
        absent_days = sum(1 for a in attendances if a.status == 'absent')
        late_days = sum(1 for a in attendances if a.status == 'late')
        total_days = len(attendances)
        
        report.append({
            'student_id': student.id,
            'admission_number': student.admission_number,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'class_id': student.class_id,
            'class_name': student.class_.name if student.class_ else None,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'total_days': total_days,
            'attendance_rate': round((present_days / total_days * 100), 2) if total_days > 0 else 0
        })
    
    return jsonify(report), 200

@attendance_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    month = request.args.get('month')
    year = request.args.get('year')
    
    query = Attendance.query.filter_by(student_id=student_id)
    
    if month and year:
        try:
            month = int(month)
            year = int(year)
            query = query.filter(
                db.extract('year', Attendance.date) == year,
                db.extract('month', Attendance.date) == month
            )
        except ValueError:
            return jsonify({'message': 'Month and year must be numbers'}), 400
    
    attendances = query.order_by(Attendance.date).all()
    
    attendance_data = [{
        'id': attendance.id,
        'date': attendance.date.isoformat(),
        'status': attendance.status,
        'remarks': attendance.remarks
    } for attendance in attendances]
    
    return jsonify(attendance_data), 200