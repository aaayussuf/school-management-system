import random
from datetime import datetime, date, time, timedelta
from faker import Faker
from app import create_app, db
from app.models import User, Student, Class, Subject, Fee, Attendance, Timetable, Result

def create_seed_data():
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        fake = Faker()
        
        print("Creating admin and teachers...")
        # Create admin user
        admin = User(
            username='admin',
            email='admin@school.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create teachers
        teachers = []
        for i in range(1, 6):
            teacher = User(
                username=f'teacher{i}',
                email=f'teacher{i}@school.com',
                role='teacher',
                is_active=True
            )
            teacher.set_password(f'teacher{i}123')
            teachers.append(teacher)
            db.session.add(teacher)
        
        db.session.commit()
        
        print("Creating classes...")
        # Create classes
        classes = []
        class_names = ['Nursery', 'KG', 'Class 1', 'Class 2', 'Class 3', 
                      'Class 4', 'Class 5', 'Class 6', 'Class 7', 'Class 8']
        
        for i, name in enumerate(class_names):
            class_ = Class(
                name=name,
                teacher_id=teachers[i % len(teachers)].id if i < len(teachers) else None
            )
            classes.append(class_)
            db.session.add(class_)
        
        db.session.commit()
        
        print("Creating subjects...")
        # Create subjects
        subjects = []
        subject_names = [
            ('Mathematics', 'MATH'), ('English', 'ENG'), ('Science', 'SCI'),
            ('Social Studies', 'SOC'), ('Computer Science', 'COMP'), 
            ('Art', 'ART'), ('Music', 'MUS'), ('Physical Education', 'PE'),
            ('History', 'HIST'), ('Geography', 'GEOG')
        ]
        
        for name, code in subject_names:
            subject = Subject(
                name=name,
                code=code
            )
            subjects.append(subject)
            db.session.add(subject)
        
        db.session.commit()
        
        print("Creating students...")
        # Create students
        students = []
        for i in range(1, 101):
            admission_date = fake.date_between(start_date='-5y', end_date='today')
            dob = fake.date_of_birth(minimum_age=4, maximum_age=18)
            
            student = Student(
                admission_number=f'ADM-{str(i).zfill(4)}',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=dob,
                gender=random.choice(['Male', 'Female']),
                address=fake.address(),
                phone=fake.phone_number(),
                email=fake.email(),
                class_id=random.choice(classes).id,
                admission_date=admission_date,
                is_active=random.choices([True, False], weights=[90, 10])[0]
            )
            students.append(student)
            db.session.add(student)
        
        db.session.commit()
        
        print("Creating fees...")
        # Create fee records
        terms = ['Term 1 2023', 'Term 2 2023', 'Term 3 2023', 'Term 1 2024']
        for student in random.sample(students, 80):  # 80% of students have fees
            for term in random.sample(terms, random.randint(1, 3)):  # 1-3 terms per student
                fee = Fee(
                    student_id=student.id,
                    amount=random.randint(5000, 20000),
                    payment_date=fake.date_between(
                        start_date=datetime.strptime(term.split()[2] + '-' + 
                                                    {'Term 1': '01', 'Term 2': '05', 'Term 3': '09'}[' '.join(term.split()[:2])] + '-01', '%Y-%m-%d'),
                        end_date='today'
                    ),
                    term=term,
                    payment_method=random.choice(['Cash', 'Cheque', 'Bank Transfer', 'Mobile Money']),
                    receipt_number=f'RCP-{random.randint(1000, 9999)}',
                    notes=fake.sentence() if random.random() > 0.7 else None
                )
                db.session.add(fee)
        
        db.session.commit()
        
        print("Creating attendance records...")
        # Create attendance records
        for student in random.sample(students, 90):  # 90% of students have attendance
            for _ in range(random.randint(5, 30)):  # 5-30 attendance records per student
                attendance = Attendance(
                    student_id=student.id,
                    date=fake.date_between(start_date='-1y', end_date='today'),
                    status=random.choices(
                        ['present', 'absent', 'late'],
                        weights=[80, 15, 5]
                    )[0],
                    remarks=fake.sentence() if random.random() > 0.8 else None
                )
                db.session.add(attendance)
        
        db.session.commit()
        
        print("Creating timetable...")
        # Create timetable
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = [
            ('08:00', '09:00'), ('09:00', '10:00'), ('10:30', '11:30'),
            ('11:30', '12:30'), ('13:30', '14:30'), ('14:30', '15:30')
        ]
        
        for class_ in classes:
            for day in days_of_week:
                # 3-5 subjects per day
                for start, end in random.sample(time_slots, random.randint(3, 5)):
                    timetable = Timetable(
                        class_id=class_.id,
                        subject_id=random.choice(subjects).id,
                        day_of_week=day,
                        start_time=datetime.strptime(start, '%H:%M').time(),
                        end_time=datetime.strptime(end, '%H:%M').time(),
                        teacher_id=random.choice(teachers).id
                    )
                    db.session.add(timetable)
        
        db.session.commit()
        
        print("Creating results...")
        # Create results
        for student in random.sample(students, 70):  # 70% of students have results
            for term in random.sample(terms, random.randint(1, 3)):  # 1-3 terms per student
                for subject in random.sample(subjects, random.randint(3, 8)):  # 3-8 subjects per term
                    marks = random.randint(30, 100)
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
                        student_id=student.id,
                        subject_id=subject.id,
                        term=term,
                        marks=marks,
                        grade=grade,
                        remarks=fake.sentence() if random.random() > 0.7 else None
                    )
                    db.session.add(result)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    create_seed_data()