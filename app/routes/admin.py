from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app.models import db, User, Appointment
from app.forms import AdminEditUserForm, RegistrationForm, AppointmentForm, AdminUserForm
from functools import wraps
from datetime import datetime
from flask_bcrypt import Bcrypt
import csv
import io

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
bcrypt = Bcrypt()

# Admin role checks
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'superadmin']:
            flash('Admin access only.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper

def superadmin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'superadmin':
            flash('Super admin access only.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return wrapper

# Admin Dashboard
@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users = User.query.order_by(User.username).all()
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin/admin_dashboard.html', user=current_user, users=users, appointments=appointments)

# Edit User
@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_user.html', form=form, user=user)

# Delete User
@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'superadmin':
        flash('Cannot delete a superadmin.', 'warning')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

# Create User
@admin_bp.route('/user/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = AdminUserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('User already exists.', 'danger')
            return redirect(url_for('admin.create_user'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, role=role, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_user.html', form=form)

# Create Appointment
@admin_bp.route('/appointment/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_appointment():
    form = AppointmentForm()
    form.patient_id.choices = [(p.id, f"{p.username} ({p.email})") for p in User.query.filter_by(role='patient').all()]
    form.doctor_id.choices = [(0, '-- Unassigned --')] + [(d.id, f"{d.username} ({d.email})") for d in User.query.filter_by(role='doctor').all()]

    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data if form.doctor_id.data != 0 else None,
            reason=form.reason.data,
            date=form.date.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('/admin/create_appointment.html', form=form)

# Edit Appointment
@admin_bp.route('/appointment/edit/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)
    form.patient_id.choices = [(p.id, f"{p.username} ({p.email})") for p in User.query.filter_by(role='patient').all()]
    form.doctor_id.choices = [(0, '-- Unassigned --')] + [(d.id, f"{d.username} ({d.email})") for d in User.query.filter_by(role='doctor').all()]

    if request.method == 'GET' and appointment.doctor_id is None:
        form.doctor_id.data = 0

    if form.validate_on_submit():
        appointment.patient_id = form.patient_id.data
        appointment.doctor_id = form.doctor_id.data if form.doctor_id.data != 0 else None
        appointment.reason = form.reason.data
        appointment.date = form.date.data
        db.session.commit()
        flash('Appointment updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_appointment.html', form=form, appointment=appointment)

# Delete Appointment
@admin_bp.route('/appointment/delete/<int:appointment_id>', methods=['POST'])
@login_required
@admin_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))

# Export Users to CSV
@admin_bp.route('/export/users')
@login_required
@admin_required
def export_users():
    users = User.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Username', 'Email', 'Role'])
    for u in users:
        writer.writerow([u.id, u.username, u.email, u.role])
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=users.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

# Export Appointments to CSV
@admin_bp.route('/export/appointments')
@login_required
@admin_required
def export_appointments():
    appointments = Appointment.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Patient ID', 'Doctor ID', 'Reason', 'Date'])
    for a in appointments:
        writer.writerow([a.id, a.patient_id, a.doctor_id, a.reason, a.date])
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=appointments.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

