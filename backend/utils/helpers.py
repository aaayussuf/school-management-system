from datetime import datetime, date
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

def validate_date(date_str, format='%Y-%m-%d'):
    try:
        return datetime.strptime(date_str, format).date()
    except ValueError:
        return None

def validate_time(time_str, format='%H:%M'):
    try:
        return datetime.strptime(time_str, format).time()
    except ValueError:
        return None

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def teacher_or_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] not in ['admin', 'teacher']:
            return jsonify({'message': 'Teacher or admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def paginate(query, schema):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': schema.dump(paginated.items),
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page
    }