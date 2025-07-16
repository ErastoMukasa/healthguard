from app import db
from datetime import datetime

class DoctorMessage(db.Model):
    __tablename__ = 'doctor_messages'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_from_patient = db.Column(db.Boolean, nullable=False, default=False)  # NEW flag

    # Relationships
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='doctor_sent_messages')
    patient = db.relationship('User', foreign_keys=[patient_id], backref='doctor_received_messages')
