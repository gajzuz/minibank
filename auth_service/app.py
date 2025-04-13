from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = "your-secret-key"

# --- Database Config ---
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@"
    f"{os.environ['DB_HOST']}:5432/{os.environ['DB_NAME']}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)


# --- User Model ---
class User(db.Model, UserMixin):
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(200), nullable=False)


# --- Load user for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# --- Initialize Database with One User ---
@app.before_request
def ensure_db_setup():
    if not hasattr(app, "db_initialized"):
        with app.app_context():
            db.create_all()
            if not User.query.get("user1"):
                db.session.add(User(id="user1", password="password123"))
                db.session.commit()
        app.db_initialized = True


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("account"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/account")
@login_required
def account():
    user_id = current_user.id
    try:
        response = requests.get(
            f"http://transaction-service:5006/transactions/{user_id}"
        )
        transactions = response.json()
    except Exception as e:
        print(f"Error contacting transaction service: {e}")
        transactions = []

    return render_template("account.html", user=user_id, transactions=transactions)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
