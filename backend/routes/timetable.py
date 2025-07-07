from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Timetable, Class, Subject, User

timetable_bp = Blueprint('timetable_bp', __name__)

@timetable_bp.route('/', methods=['GET'])
@jwt_required()
def get_timetable():
    current_user = get_jwt_identity()
    if current_user['role'] not in ['admin', 'teacher']:
        return jsonify({'message': 'Unauthorized access'}), 403
    
    class_id = request.args.get('class_id')
    teacher_id = request.args.get('teacher_id')
    
    query = Timetable.query
    
    if class_id:
        query = query.filter_by(class_id=class_id)
    if teacher_id:
        query = query.filter_by(teacher_id=teacher_id)
    
    timetable = query.order_by(Timetable.day_of_week, Timetable.start_time).all()
    
    timetable_data = [{
        'id': item.id,
        'class_id': item.class_id,
        'class_name': item.class_.name if item.class_ else None,
        'subject_id': item.subject_id,
        'subject_name': item.subject.name if item.subject else None,
        'day_of_week': item.day_of_week,
        'start_time': item.start_time.strftime('%H:%M') if item.start_time else None,
        'end_time': item.end_time.strftime('%H:%M') if item.end_time else None,
        'teacher_id': item.teacher_id,
        'teacher_name': f"{item.teacher.first_name} {item.teacher.last_name}" if item.teacher else None
    } for item in timetable]
    
    return jsonify(timetable_data), 200

@timetable_bp.route('/', methods=['POST'])
@jwt_required()
def create_timetable_entry():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    data = request.get_json()
    
    required_fields = ['class_id', 'subject_id', 'day_of_week', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        # Validate time format
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use HH:MM'}), 400
    
    # Check for overlapping timetable entries
    overlapping = Timetable.query.filter(
        Timetable.class_id == data['class_id'],
        Timetable.day_of_week == data['day_of_week'],
        Timetable.start_time < end_time,
        Timetable.end_time > start_time
    ).first()
    
    if overlapping:
        return jsonify({
            'message': 'Timetable entry overlaps with existing entry',
            'conflict_with': {
                'subject': overlapping.subject.name,
                'teacher': f"{overlapping.teacher.first_name} {overlapping.teacher.last_name}" if overlapping.teacher else None,
                'time': f"{overlapping.start_time.strftime('%H:%M')}-{overlapping.end_time.strftime('%H:%M')}"
            }
        }), 400
    
    timetable = Timetable(
        class_id=data['class_id'],
        subject_id=data['subject_id'],
        day_of_week=data['day_of_week'],
        start_time=start_time,
        end_time=end_time,
        teacher_id=data.get('teacher_id')
    )
    
    db.session.add(timetable)
    db.session.commit()
    
    return jsonify({'message': 'Timetable entry created successfully', 'id': timetable.id}), 201

@timetable_bp.route('/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_timetable_entry(entry_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    timetable = Timetable.query.get_or_404(entry_id)
    data = request.get_json()
    
    try:
        if 'start_time' in data:
            timetable.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            timetable.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use HH:MM'}), 400
    
    timetable.class_id = data.get('class_id', timetable.class_id)
    timetable.subject_id = data.get('subject_id', timetable.subject_id)
    timetable.day_of_week = data.get('day_of_week', timetable.day_of_week)
    timetable.teacher_id = data.get('teacher_id', timetable.teacher_id)
    
    db.session.commit()
    
    return jsonify({'message': 'Timetable entry updated successfully'}), 200

@timetable_bp.route('/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_timetable_entry(entry_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    timetable = Timetable.query.get_or_404(entry_id)
    
    db.session.delete(timetable)
    db.session.commit()
    
    return jsonify({'message': 'Timetable entry deleted successfully'}), 200