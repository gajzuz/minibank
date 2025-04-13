from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# PostgreSQL config from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@"
    f"{os.environ['DB_HOST']}:5432/{os.environ['DB_NAME']}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)


@app.before_request
def ensure_db_setup():
    if not hasattr(app, "db_initialized"):
        with app.app_context():
            db.create_all()

            if not Transaction.query.first():
                db.session.add_all(
                    [
                        Transaction(
                            user_id="user1",
                            desc="Grocery",
                            amount=-45.60,
                            date="2025-04-01",
                        ),
                        Transaction(
                            user_id="user1",
                            desc="Salary",
                            amount=2500.00,
                            date="2025-03-31",
                        ),
                        Transaction(
                            user_id="user2",
                            desc="Gym",
                            amount=-30.00,
                            date="2025-04-02",
                        ),
                    ]
                )
                db.session.commit()

        app.db_initialized = True


@app.route("/transactions/<user_id>", methods=["GET"])
def get_transactions(user_id):
    txns = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([{"desc": t.desc, "amount": t.amount, "date": t.date} for t in txns])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
