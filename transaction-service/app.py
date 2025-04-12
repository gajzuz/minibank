# transaction - service / transaction_service.py

from flask import Flask, jsonify

app = Flask(__name__)

# Mock transaction data
transactions = {
    "user1": [
        {"desc": "Grocery", "amount": -45.60, "date": "2025-04-01"},
        {"desc": "Salary", "amount": 2500.00, "date": "2025-03-31"},
    ],
    "user2": [{"desc": "Gym", "amount": -30.00, "date": "2025-04-02"}],
}


@app.route("/transactions/<user_id>", methods=["GET"])
def get_transactions(user_id):
    return jsonify(transactions.get(user_id, []))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
