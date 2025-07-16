from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.health_data import HealthData
from app.models.doctor_message import DoctorMessage
from app.models.appointment import Appointment
from app.forms.forms import HealthDataForm, AppointmentForm, PatientMessageForm
from app.models.user import User
from app import db

# Import the AI risk prediction function
from app.ai.predict_risk import predict_risk

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'patient':
        return "Unauthorized", 403

    form = HealthDataForm()
    appointment_form = AppointmentForm()
    patient_message_form = PatientMessageForm()

    # Populate doctor choices for patient message form dropdown
    doctors = User.query.filter_by(role='doctor').all()
    if doctors:
        patient_message_form.doctor_id.choices = [(doctor.id, doctor.username) for doctor in doctors]
    else:
        patient_message_form.doctor_id.choices = [(-1, 'No doctors available')]

    # Populate patient choices for appointment_form.patient_id (fixed to current user)
    appointment_form.patient_id.choices = [(current_user.id, current_user.username)]

    # Populate doctor choices for appointment_form.doctor_id
    if doctors:
        appointment_form.doctor_id.choices = [(doctor.id, doctor.username) for doctor in doctors]
    else:
        appointment_form.doctor_id.choices = [(-1, 'No doctors available')]

    # Handle health data form submission
    if form.validate_on_submit() and 'submit' in request.form:
        # Extract systolic blood pressure for AI input
        bp_systolic = None
        if form.blood_pressure.data and '/' in form.blood_pressure.data:
            try:
                bp_systolic = int(form.blood_pressure.data.split('/')[0])
            except ValueError:
                bp_systolic = None

        # Call the AI prediction function
        risk_class, risk_prob = predict_risk(
            temperature=form.temperature.data,
            heart_rate=form.heart_rate.data,
            oxygen_level=form.oxygen_level.data,
            glucose_level=form.glucose_level.data,
            blood_pressure=bp_systolic
        )

        # Create and save the health data entry with AI results
        entry = HealthData(
            patient_id=current_user.id,
            temperature=form.temperature.data,
            heart_rate=form.heart_rate.data,
            oxygen_level=form.oxygen_level.data,
            blood_pressure=form.blood_pressure.data,
            glucose_level=form.glucose_level.data,
            risk_score=risk_prob,
            risk_class="High Risk" if risk_class else "Low Risk"
        )
        db.session.add(entry)
        db.session.commit()

        flash(f'Health data submitted successfully! AI Risk Score: {risk_prob:.2f} ({"High Risk" if risk_class else "Low Risk"})', 'success')
        return redirect(url_for('patient.dashboard'))

    # Handle appointment form submission
    if appointment_form.validate_on_submit() and 'book' in request.form:
        appointment = Appointment(
            patient_id=current_user.id,
            reason=appointment_form.reason.data,
            date=appointment_form.date.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.dashboard'))

    # Handle patient message form submission
    if patient_message_form.validate_on_submit() and 'send_message' in request.form:
        message = DoctorMessage(
            patient_id=current_user.id,
            doctor_id=patient_message_form.doctor_id.data,
            content=patient_message_form.content.data,
            is_from_patient=True  # Mark this message as from patient
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent to your doctor successfully!', 'success')
        return redirect(url_for('patient.dashboard'))

    # Query health data for this patient, ordered by timestamp ascending
    health_data_entries = HealthData.query.filter_by(patient_id=current_user.id).order_by(HealthData.timestamp.asc()).all()

    # Prepare data for chart.js
    labels = [entry.timestamp.strftime("%Y-%m-%d %H:%M") for entry in health_data_entries]
    temperatures = [entry.temperature for entry in health_data_entries]
    heart_rates = [entry.heart_rate for entry in health_data_entries]
    oxygen_levels = [entry.oxygen_level for entry in health_data_entries]

    # Extract only the systolic value (first number) from blood pressure for charting
    blood_pressures = [
        int(entry.blood_pressure.split('/')[0]) if entry.blood_pressure and '/' in entry.blood_pressure else None
        for entry in health_data_entries
    ]

    glucose_levels = [entry.glucose_level for entry in health_data_entries]

    # Query doctor's messages for this patient (only messages from doctors)
    doctor_messages = DoctorMessage.query.filter_by(
        patient_id=current_user.id,
        is_from_patient=False
    ).order_by(DoctorMessage.timestamp.desc()).all()

    return render_template(
        'patient_dashboard.html',
        user=current_user,
        form=form,
        appointment_form=appointment_form,
        patient_message_form=patient_message_form,
        labels=labels,
        temperatures=temperatures,
        heart_rates=heart_rates,
        oxygen_levels=oxygen_levels,
        blood_pressures=blood_pressures,
        glucose_levels=glucose_levels,
        doctor_messages=doctor_messages
    )
