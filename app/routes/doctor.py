from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app.models import db, User, HealthData, DoctorMessage
from app.forms.forms import DoctorMessageForm

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@doctor_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'doctor':
        return "Unauthorized", 403

    form = DoctorMessageForm()
    patients = User.query.filter_by(role='patient').all()

    # Sort patient health data by timestamp descending
    for patient in patients:
        patient.health_data.sort(key=lambda r: r.timestamp, reverse=True)

    # Messages from patients (not from doctor)
    patient_messages = DoctorMessage.query.filter_by(
        doctor_id=current_user.id,
        is_from_patient=True
    ).order_by(DoctorMessage.timestamp.desc()).all()

    if form.validate_on_submit():
        patient_id = request.form.get('patient_id')
        content = form.content.data
        if patient_id and content:
            message = DoctorMessage(
                patient_id=patient_id,
                doctor_id=current_user.id,
                content=content,
                is_from_patient=False  # from doctor
            )
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('doctor.dashboard'))

    return render_template(
        'doctor_dashboard.html',
        user=current_user,
        patients=patients,
        form=form,
        patient_messages=patient_messages
    )

@doctor_bp.route('/export/patient-results')
@login_required
def export_patient_results():
    from io import StringIO
    import csv

    patients = User.query.filter_by(role='patient').all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Patient', 'Temperature', 'Heart Rate', 'Oxygen Level',
        'Glucose Level', 'Blood Pressure', 'Risk Score', 'Risk Class', 'Timestamp'
    ])

    for patient in patients:
        for record in sorted(patient.health_data, key=lambda r: r.timestamp, reverse=True):
            if record.risk_score is not None:
                risk_label = 'High Risk' if record.risk_class == 1 else 'Low Risk'
                writer.writerow([
                    patient.username,
                    record.temperature,
                    record.heart_rate,
                    record.oxygen_level,
                    record.glucose_level or '',
                    record.blood_pressure or '',
                    f"{record.risk_score:.2f}",
                    risk_label,
                    record.timestamp.strftime('%Y-%m-%d %H:%M')
                ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=patient_results.csv'
    response.headers['Content-type'] = 'text/csv'
    return response
