from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Fee, Student
from datetime import datetime

fees_bp = Blueprint('fees_bp', __name__)

@fees_bp.route('/', methods=['GET'])
@jwt_required()
def get_fees():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    student_id = request.args.get('student_id')
    term = request.args.get('term')
    
    query = Fee.query
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    if term:
        query = query.filter_by(term=term)
    
    fees = query.order_by(Fee.payment_date.desc()).all()
    
    fees_data = [{
        'id': fee.id,
        'student_id': fee.student_id,
        'student_name': f"{fee.student.first_name} {fee.student.last_name}",
        'admission_number': fee.student.admission_number,
        'amount': fee.amount,
        'payment_date': fee.payment_date.isoformat() if fee.payment_date else None,
        'term': fee.term,
        'payment_method': fee.payment_method,
        'receipt_number': fee.receipt_number,
        'notes': fee.notes
    } for fee in fees]
    
    return jsonify(fees_data), 200

@fees_bp.route('/unpaid', methods=['GET'])
@jwt_required()
def get_unpaid_students():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    term = request.args.get('term', 'Term 1 2023')  # Default to current term
    
    # Get all active students
    all_students = Student.query.filter_by(is_active=True).all()
    
    # Get students who have paid for the term
    paid_student_ids = [fee.student_id for fee in Fee.query.filter_by(term=term).all()]
    
    unpaid_students = [student for student in all_students if student.id not in paid_student_ids]
    
    unpaid_students_data = [{
        'id': student.id,
        'admission_number': student.admission_number,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'class_id': student.class_id,
        'class_name': student.class_.name if student.class_ else None
    } for student in unpaid_students]
    
    return jsonify(unpaid_students_data), 200

@fees_bp.route('/', methods=['POST'])
@jwt_required()
def record_payment():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    required_fields = ['student_id', 'amount', 'term']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    student = Student.query.get(data['student_id'])
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    fee = Fee(
        student_id=data['student_id'],
        amount=data['amount'],
        term=data['term'],
        payment_method=data.get('payment_method'),
        receipt_number=data.get('receipt_number'),
        notes=data.get('notes')
    )
    
    db.session.add(fee)
    db.session.commit()
    
    return jsonify({'message': 'Payment recorded successfully', 'id': fee.id}), 201

@fees_bp.route('/<int:fee_id>', methods=['PUT'])
@jwt_required()
def update_payment(fee_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    fee = Fee.query.get_or_404(fee_id)
    data = request.get_json()
    
    fee.amount = data.get('amount', fee.amount)
    fee.term = data.get('term', fee.term)
    fee.payment_method = data.get('payment_method', fee.payment_method)
    fee.receipt_number = data.get('receipt_number', fee.receipt_number)
    fee.notes = data.get('notes', fee.notes)
    
    if 'payment_date' in data:
        try:
            fee.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Payment updated successfully'}), 200