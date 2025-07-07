from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.students import students_bp
    from routes.fees import fees_bp
    from routes.attendance import attendance_bp
    from routes.timetable import timetable_bp
    from routes.results import results_bp
    from routes.index import main_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(fees_bp, url_prefix='/api/fees')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(timetable_bp, url_prefix='/api/timetable')
    app.register_blueprint(results_bp, url_prefix='/api/results')

    app.register_blueprint(main_bp)

    return app
