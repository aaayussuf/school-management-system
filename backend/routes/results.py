from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Result, Student, Subject
from datetime import datetime

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/', methods=['GET'])
@jwt_required()
def get_results():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    student_id = request.args.get('student_id')
    subject_id = request.args.get('subject_id')
    term = request.args.get('term')
    class_id = request.args.get('class_id')
    
    query = Result.query
    
    if student_id:
        query = query.filter_by(student_id=student_id)
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
    if term:
        query = query.filter_by(term=term)
    if class_id:
        query = query.join(Student).filter(Student.class_id == class_id)
    
    results = query.order_by(Result.term).all()
    
    results_data = [{
        'id': result.id,
        'student_id': result.student_id,
        'student_name': f"{result.student.first_name} {result.student.last_name}",
        'admission_number': result.student.admission_number,
        'subject_id': result.subject_id,
        'subject_name': result.subject.name,
        'term': result.term,
        'marks': result.marks,
        'grade': result.grade,
        'remarks': result.remarks
    } for result in results]
    
    return jsonify(results_data), 200

@results_bp.route('/', methods=['POST'])
@jwt_required()
def create_result():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    required_fields = ['student_id', 'subject_id', 'term', 'marks']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if result already exists for this student, subject, and term
    existing = Result.query.filter_by(
        student_id=data['student_id'],
        subject_id=data['subject_id'],
        term=data['term']
    ).first()
    
    if existing:
        return jsonify({'message': 'Result already exists for this student, subject, and term'}), 400
    
    # Calculate grade based on marks (simple example)
    marks = float(data['marks'])
    if marks >= 80:
        grade = 'A'
    elif marks >= 70:
        grade = 'B'
    elif marks >= 60:
        grade = 'C'
    elif marks >= 50:
        grade = 'D'
    else:
        grade = 'F'
    
    result = Result(
        student_id=data['student_id'],
        subject_id=data['subject_id'],
        term=data['term'],
        marks=marks,
        grade=grade,
        remarks=data.get('remarks')
    )
    
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'message': 'Result created successfully', 'id': result.id}), 201

@results_bp.route('/<int:result_id>', methods=['PUT'])
@jwt_required()
def update_result(result_id):
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    result = Result.query.get_or_404(result_id)
    data = request.get_json()
    
    if 'marks' in data:
        marks = float(data['marks'])
        result.marks = marks
        
        # Recalculate grade
        if marks >= 80:
            result.grade = 'A'
        elif marks >= 70:
            result.grade = 'B'
        elif marks >= 60:
            result.grade = 'C'
        elif marks >= 50:
            result.grade = 'D'
        else:
            result.grade = 'F'
    
    result.term = data.get('term', result.term)
    result.remarks = data.get('remarks', result.remarks)
    
    db.session.commit()
    
    return jsonify({'message': 'Result updated successfully'}), 200

@results_bp.route('/report-card/<int:student_id>', methods=['GET'])
@jwt_required()
def generate_report_card(student_id):
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    term = request.args.get('term')
    if not term:
        return jsonify({'message': 'Term is required'}), 400
    
    # Get student info
    student = Student.query.get_or_404(student_id)
    
    # Get all results for the student in the specified term
    results = Result.query.filter_by(
        student_id=student_id,
        term=term
    ).all()
    
    # Get attendance summary for the term
    # (Assuming term corresponds to a date range - you'll need to implement this logic)
    # attendance = calculate_attendance_summary(student_id, term)
    
    # Generate PDF (placeholder - implement this in utils/pdf_generator.py)
    # pdf_data = generate_pdf_report_card(student, results, attendance)
    
    # For now, return JSON data
    report_card = {
        'student': {
            'id': student.id,
            'admission_number': student.admission_number,
            'name': f"{student.first_name} {student.last_name}",
            'class': student.class_.name if student.class_ else None,
        },
        'term': term,
        'results': [{
            'subject': result.subject.name,
            'marks': result.marks,
            'grade': result.grade,
            'remarks': result.remarks
        } for result in results],
        # 'attendance': attendance,
        'generated_on': datetime.utcnow().isoformat()
    }
    
    return jsonify(report_card), 200