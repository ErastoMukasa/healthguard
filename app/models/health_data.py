from app import db
from datetime import datetime

class HealthData(db.Model):
    __tablename__ = 'health_data'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    temperature = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)
    oxygen_level = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(15))  # New
    glucose_level = db.Column(db.Float)   
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    risk_score = db.Column(db.Float, nullable=True)  # e.g., probability from 0 to 1
    risk_class = db.Column(db.String(10), nullable=True)  # e.g., 'low' or 'high'

