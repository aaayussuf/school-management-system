from datetime import datetime
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'teacher'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    admission_date = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    class_ = db.relationship('Class', back_populates='students')
    fees = db.relationship('Fee', back_populates='student')
    attendances = db.relationship('Attendance', back_populates='student')
    results = db.relationship('Result', back_populates='student')

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    students = db.relationship('Student', back_populates='class_')
    teacher = db.relationship('User')
    timetables = db.relationship('Timetable', back_populates='class_')

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    
    timetables = db.relationship('Timetable', back_populates='subject')
    results = db.relationship('Result', back_populates='subject')

class Fee(db.Model):
    __tablename__ = 'fees'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=datetime.utcnow)
    term = db.Column(db.String(20), nullable=False)  # e.g., "Term 1 2023"
    payment_method = db.Column(db.String(50))
    receipt_number = db.Column(db.String(50), unique=True)
    notes = db.Column(db.Text)
    
    student = db.relationship('Student', back_populates='fees')

class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'present', 'absent', 'late'
    remarks = db.Column(db.String(200))
    
    student = db.relationship('Student', back_populates='attendances')

class Timetable(db.Model):
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)  # 'Monday', 'Tuesday', etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    class_ = db.relationship('Class', back_populates='timetables')
    subject = db.relationship('Subject', back_populates='timetables')
    teacher = db.relationship('User')

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    term = db.Column(db.String(20), nullable=False)  # e.g., "Term 1 2023"
    marks = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2))
    remarks = db.Column(db.String(200))
    
    student = db.relationship('Student', back_populates='results')
    subject = db.relationship('Subject', back_populates='results')