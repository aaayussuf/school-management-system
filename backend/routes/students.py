from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Student, Class
from datetime import datetime

students_bp = Blueprint('students_bp', __name__)

@students_bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    class_id = request.args.get('class_id')
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    query = Student.query.filter_by(is_active=is_active)
    
    if class_id:
        query = query.filter_by(class_id=class_id)
    
    students = query.all()
    
    students_data = [{
        'id': student.id,
        'admission_number': student.admission_number,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
        'gender': student.gender,
        'class_id': student.class_id,
        'class_name': student.class_.name if student.class_ else None,
        'admission_date': student.admission_date.isoformat() if student.admission_date else None
    } for student in students]
    
    return jsonify(students_data), 200

@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    student = Student.query.get_or_404(student_id)
    
    student_data = {
        'id': student.id,
        'admission_number': student.admission_number,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
        'gender': student.gender,
        'address': student.address,
        'phone': student.phone,
        'email': student.email,
        'class_id': student.class_id,
        'class_name': student.class_.name if student.class_ else None,
        'admission_date': student.admission_date.isoformat() if student.admission_date else None,
        'is_active': student.is_active
    }
    
    return jsonify(student_data), 200

@students_bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    required_fields = ['admission_number', 'first_name', 'last_name', 'date_of_birth', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if Student.query.filter_by(admission_number=data['admission_number']).first():
        return jsonify({'message': 'Admission number already exists'}), 400
    
    try:
        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    student = Student(
        admission_number=data['admission_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=date_of_birth,
        gender=data['gender'],
        address=data.get('address'),
        phone=data.get('phone'),
        email=data.get('email'),
        class_id=data.get('class_id'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'message': 'Student created successfully', 'id': student.id}), 201

@students_bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    
    if 'admission_number' in data and data['admission_number'] != student.admission_number:
        if Student.query.filter_by(admission_number=data['admission_number']).first():
            return jsonify({'message': 'Admission number already exists'}), 400
        student.admission_number = data['admission_number']
    
    if 'date_of_birth' in data:
        try:
            student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.gender = data.get('gender', student.gender)
    student.address = data.get('address', student.address)
    student.phone = data.get('phone', student.phone)
    student.email = data.get('email', student.email)
    student.class_id = data.get('class_id', student.class_id)
    student.is_active = data.get('is_active', student.is_active)
    
    db.session.commit()
    
    return jsonify({'message': 'Student updated successfully'}), 200

@students_bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    student = Student.query.get_or_404(student_id)
    
    # Soft delete by setting is_active to False
    student.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Student deactivated successfully'}), 200