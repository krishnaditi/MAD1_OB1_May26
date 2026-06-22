from flask import Flask, render_template
from models import db, Admin, Doctor, Patient, Department, Appointment, Treatment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_management.db'
app.config['SECRET_KEY'] = 'Aditi123#'

db.init_app(app)

with app.app_context():
    db.create_all()

def make_admin():
    with app.app_context():
        admin = Admin(username="Aditi", email="aditi@gmail.com", password="Admin123")
        if not Admin.query.first():
            db.session.add(admin)
            db.session.commit()

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    make_admin()
    app.run()
