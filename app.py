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
            new_patient = Patient(name=name, email=email, password=hashed_password)
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Patient.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for("patient_dashboard"))

    return render_template("login.html")

@app.route("/patient_dashboard", methods=["GET"])
def patient_dashboard():
    return render_template("patient_dashboard.html")

if __name__ == "__main__":
    make_admin()
    app.run()
