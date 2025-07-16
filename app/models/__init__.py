from app.models.user import User
from app.models.health_data import HealthData
from app.models.doctor_message import DoctorMessage
from app.models.patient_message import PatientMessage  # ✅ Add this line
from .appointment import Appointment  
# Optional: only if you want to import db from app.models
from app import db

__all__ = ['User', 'HealthData', 'DoctorMessage', 'PatientMessage', 'db']

