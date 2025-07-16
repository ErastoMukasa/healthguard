HealthGuard – AI-Powered Health Monitoring Platform
HealthGuard** is a smart healthcare web application that enables real-time patient monitoring using AI risk classification. It includes dashboards for **patients**, **doctors**, and **admins**, offering vital data tracking, messaging, appointment booking, and CSV exports.

Features

Secure User Roles**: Admins, Doctors, and Patients with login/authentication
AI Risk Engine**: Logistic Regression classifies patients into Low/High risk
Dashboards**:
Patients: Submit vitals, view risk, book appointments
Doctors: View & export patient health summaries, send messages
Admins: Manage users/appointments and system reports
Just install Python + MySQL and run!
Export Reports**: CSV download of patients and appointments

Tech Stack

Layer	Tools
Backend:	Flask, Flask-WTF, Flask-Login
Frontend:	HTML, Bootstrap 5, Jinja2, Chart.js
AI Model:	Scikit-learn (Logistic Regression)
Database:	MySQL + SQLAlchemy (ORM)
Development IDE:	VS Code / PyCharm




Installation Guide

Requirements:  
Python 3.12+  
MySQL Server via Laragon.  
pip` installed globally

1. Clone the Repository
git clone https://github.com/ErastoMukasa/healthguard.git
cd healthguard

2. Install Python Dependencies
Install packages globally:
pip install -r requirements.txt

3. Set Up MySQL Database
1.	Open your MySQL tool (e.g., Laragon or phpMyAdmin)
2.	Create a new database named: healthguard_database
3.	Use the following credentials in config.py (or set them in app/__init__.py):
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:6AHope@localhost/healthguard_database'

4. Run Migrations
flask db init
flask db migrate
flask db upgrade

5. Launch the App
python wsgi.py

Then open your browser:
📍 http://127.0.0.1:5000/

