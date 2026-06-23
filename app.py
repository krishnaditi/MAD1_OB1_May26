from flask import Flask, render_template, request, redirect, url_for
from models import db, Admin, Doctor, Patient, Department, Appointment, Treatment
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_management.db'
app.config['SECRET_KEY'] = 'Aditi123#'

db.init_app(app)

with app.app_context():
    db.create_all()

def make_admin():
    with app.app_context():
        admin = Admin(username="Aditi", email="aditi@gmail.com", password=generate_password_hash("Admin123"))
        if not Admin.query.first():
            db.session.add(admin)
            db.session.commit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name and email and password:
            hashed_password = generate_password_hash(password)
            new_doctor = Doctor(name=name, email=email, password=hashed_password)
            new_patient = Patient(name=name, email=email, password=hashed_password)
            db.session.add(new_doctor)
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        email = request.form.get("email")
        password = request.form.get("password")

        user = Patient.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.role == 'patient':
            return redirect(url_for("patient_dashboard"))
        else:
            return render_template('login.html')

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and check_password_hash(doctor.password, password) and doctor.status == 'accepted' and doctor.role == 'doctor':
            return redirect(url_for("doctor_dashboard"))
        else:
            return render_template('login.html')

        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password) and admin.role == 'admin':
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template('login.html')

    return render_template("login.html")

@app.route("/patient_dashboard", methods=["GET"])
def patient_dashboard():
    return render_template("patient_dashboard.html")

@app.route("/doctor_dashboard", methods=["GET"])
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

@app.route("/admin_dashboard", methods=["GET"])
def admin_dashboard():
    doctor = Doctor.query.all()
    department = Department.query.all()
    return render_template("admin_dashboard.html", doctor=doctor, department=department)

@app.route("/approve_doctor/<int:doctor_id>", methods=["GET", "POST"])
def approve_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        doctor.status = 'accepted'
        db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/reject_doctor/<int:doctor_id>", methods=["GET", "POST"])
def reject_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        doctor.status = 'rejected'
        db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/create_department", methods=["GET", "POST"])
def create_department():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        
        if name and description:
            new_department = Department(name=name, description=description)
            db.session.add(new_department)
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
    return render_template("create_department.html")

@app.route("/edit_department/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):
    department = Department.query.get(department_id)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        if department and name and description:
            department.name = name
            department.description = description
            db.session.commit()
            return redirect(url_for("admin_dashboard"))
    return render_template("edit_department.html", department=department)

@app.route("/delete_department/<int:department_id>", methods=["GET", "POST"])
def delete_department(department_id):
    department = Department.query.get(department_id)
    if department:
        db.session.delete(department)
        db.session.commit()
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    make_admin()
    app.run()
