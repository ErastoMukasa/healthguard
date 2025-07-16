from app import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('User', foreign_keys=[patient_id], back_populates='appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id], back_populates='doctor_appointments')

    def __repr__(self):
        return f'<Appointment {self.id} for Patient ID {self.patient_id} with Doctor ID {self.doctor_id} on {self.date}>'
