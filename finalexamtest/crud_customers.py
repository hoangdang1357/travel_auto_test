from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ----------- DATABASE HELPER ------------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ----------- ROUTES ------------
@app.route("/")
def index():
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return render_template("customers/index.html", customers=customers)


@app.route("/add", methods=("GET", "POST"))
def add_customer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("customers/add.html")


@app.route("/edit/<int:customer_id>", methods=("GET", "POST"))
def edit_customer(customer_id):
    conn = get_db_connection()
    customer = conn.execute(
        "SELECT * FROM customers WHERE customer_id = ?", (customer_id,)
    ).fetchone()

    if not customer:
        conn.close()
        return "Customer not found", 404

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        conn.execute(
            "UPDATE customers SET name=?, email=?, phone=? WHERE customer_id=?",
            (name, email, phone, customer_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("customers/edit.html", customer=customer)


@app.route("/delete/<int:customer_id>")
def delete_customer(customer_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM customers WHERE customer_id=?", (customer_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
