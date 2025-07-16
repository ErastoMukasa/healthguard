from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField,
    FloatField, IntegerField, TextAreaField, DateTimeField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, NumberRange, Optional
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField(
        'Role',
        choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')


class HealthDataForm(FlaskForm):
    temperature = FloatField('Temperature (°C)', validators=[DataRequired(), NumberRange(min=30, max=45)])
    heart_rate = IntegerField('Heart Rate (bpm)', validators=[DataRequired(), NumberRange(min=30, max=200)])
    oxygen_level = IntegerField('Oxygen Level (%)', validators=[DataRequired(), NumberRange(min=70, max=100)])
    blood_pressure = StringField('Blood Pressure (mmHg)', validators=[DataRequired(), Length(min=3, max=15)])  # e.g., "120/80"
    glucose_level = FloatField('Glucose Level (mg/dL)', validators=[DataRequired(), NumberRange(min=50, max=500)])
    
    submit = SubmitField('Submit Health Data')


class DoctorMessageForm(FlaskForm):
    content = TextAreaField('Message to Patient', validators=[
        DataRequired(),
        Length(min=1, max=1000)
    ])
    patient_id = SelectField('Select Patient', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Send Message')


class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[Optional()])
    reason = TextAreaField('Reason for Appointment', validators=[DataRequired(), Length(min=10)])
    date = DateTimeField('Preferred Appointment Date and Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')


class PatientMessageForm(FlaskForm):
    doctor_id = SelectField('Select Doctor', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    send_message = SubmitField('Send Message')


class AdminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create User')


class AdminEditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Update User')
