from flask import Flask, render_template
from models import db, Admin, Doctor, Patient, Department, Appointment, Treatment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_management.db'
app.config['SECRET_KEY'] = 'Aditi123#'

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
