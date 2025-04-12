from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
    logout_user,
)
import requests

app = Flask(__name__, template_folder="templates")
app.secret_key = "your-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


users = {"user1": {"password": "password123"}}  # Mocked users


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            user = User(username)
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
        # REST call to transaction-service
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
