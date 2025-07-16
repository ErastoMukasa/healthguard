from datetime import datetime
from app import db

class PatientMessage(db.Model):
    __tablename__ = 'patient_messages'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    patient = db.relationship('User', foreign_keys=[patient_id], backref='messages_sent')
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='messages_received')

    def __repr__(self):
        return f'<PatientMessage from patient_id={self.patient_id} to doctor_id={self.doctor_id}>'
