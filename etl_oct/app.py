from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "bank.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables dict-like access
    return conn

@app.route("/accounts", methods=["GET"])
def get_accounts():
    account_number = request.args.get("account_number")
    conn = get_db_connection()
    cursor = conn.cursor()

    if account_number:
        cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return jsonify(dict(row)), 200
        else:
            return jsonify({"error": "Account not found"}), 404
    else:
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows]), 200

@app.route("/accounts", methods=["POST"])
def add_account():
    data = request.get_json()
    required_fields = ["account_number", "customer_name", "account_type", "balance", "last_transaction", "branch_code", "phone_number"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO accounts (account_number, customer_name, account_type, balance, last_transaction, branch_code, phone_number, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["account_number"],
            data["customer_name"].title(),
            data["account_type"],
            float(data["balance"]),
            data["last_transaction"],
            data["branch_code"],
            data["phone_number"],
            True  # Default to active
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Account added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/accounts/<int:account_number>", methods=["DELETE"])
def delete_account(account_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": f"Account {account_number} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
