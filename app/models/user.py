from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    appointments = db.relationship(
        'Appointment',
        foreign_keys='Appointment.patient_id',
        back_populates='patient',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    doctor_appointments = db.relationship(
        'Appointment',
        foreign_keys='Appointment.doctor_id',
        back_populates='doctor',
        lazy=True,
        cascade='all, delete-orphan'
    )

    health_data = db.relationship('HealthData', backref='patient', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

    def has_role(self, role_name):
        return self.role == role_name
