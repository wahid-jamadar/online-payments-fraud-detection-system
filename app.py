from flask import Flask, render_template, request, redirect, session, send_file
import mysql.connector
import pandas as pd
import joblib
import numpy as np
from config import Config
from werkzeug.security import check_password_hash

from flask_mail import Mail, Message
import random

from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

model = joblib.load("model/fraud_model.pkl")
encoder = joblib.load("model/label_encoder.pkl")


def get_db():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )


def is_logged_in():
    return "admin" in session


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and check_password_hash(user["password"], password):
        session["admin"] = username
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Invalid Credentials"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect("/")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) total FROM transactions")
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) fraud FROM transactions WHERE prediction='Fraud'"
    )
    fraud = cursor.fetchone()["fraud"]

    cursor.execute(
        "SELECT COUNT(*) safe FROM transactions WHERE prediction='Safe'"
    )
    safe = cursor.fetchone()["safe"]

    cursor.execute(
        "SELECT * FROM transactions ORDER BY id DESC LIMIT 5"
    )
    recent = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        total=total,
        fraud=fraud,
        safe=safe,
        recent=recent
    )


@app.route("/predict")
def predict():
    if not is_logged_in():
        return redirect("/")

    return render_template("predict.html")


@app.route("/predict_result", methods=["POST"])
def predict_result():
    if not is_logged_in():
        return redirect("/")

    step = int(request.form["step"])
    payment_type = request.form["type"]
    amount = float(request.form["amount"])
    oldbalanceOrg = float(request.form["oldbalanceOrg"])
    newbalanceOrig = float(request.form["newbalanceOrig"])
    oldbalanceDest = float(request.form["oldbalanceDest"])
    newbalanceDest = float(request.form["newbalanceDest"])

    encoded_type = encoder.transform([payment_type])[0]

    values = np.array([[
        step,
        encoded_type,
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest
    ]])

    pred = model.predict(values)[0]
    prob = model.predict_proba(values)[0]

    confidence = float(round(max(prob) * 100, 2))

    result = "Fraud" if pred == 1 else "Safe"

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (
        step,type,amount,
        oldbalanceOrg,newbalanceOrig,
        oldbalanceDest,newbalanceDest,
        prediction,confidence
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        step,payment_type,amount,
        oldbalanceOrg,newbalanceOrig,
        oldbalanceDest,newbalanceDest,
        result,confidence
    ))

    db.commit()
    cursor.close()
    db.close()

    if result == "Fraud":
        try:
            msg = Message(
                "Fraud Alert Detected",
                recipients=[Config.MAIL_DEFAULT_SENDER]
            )
            msg.body = f"Suspicious transaction detected. Amount: {amount}"
            mail.send(msg)
        except Exception as e:
            print(f"Mail sending failed: {e}")

    return render_template(
        "result.html",
        result=result,
        confidence=confidence
    )


@app.route("/history")
def history():
    if not is_logged_in():
        return redirect("/")

    page = int(request.args.get("page", 1))
    search = request.args.get("search", "")

    limit = 10
    offset = (page - 1) * limit

    db = get_db()
    cursor = db.cursor(dictionary=True)

    sql = """
    SELECT * FROM transactions
    WHERE type LIKE %s OR prediction LIKE %s
    ORDER BY id DESC
    LIMIT %s OFFSET %s
    """

    cursor.execute(
        sql,
        (f"%{search}%", f"%{search}%", limit, offset)
    )

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "history.html",
        rows=rows,
        page=page,
        search=search
    )


@app.route("/export")
def export():
    if not is_logged_in():
        return redirect("/")

    db = get_db()

    df = pd.read_sql(
        "SELECT * FROM transactions",
        db
    )

    file = "transactions_export.csv"
    df.to_csv(file, index=False)

    db.close()

    return send_file(file, as_attachment=True)

@app.route("/delete/<int:id>")
def delete(id):
    if not is_logged_in():
        return redirect("/")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=%s",
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/history")

# Send OTP Route
@app.route("/send_otp")
def send_otp():
    otp = str(random.randint(100000, 999999))
    session["otp"] = otp

    msg = Message(
        "Your Login OTP",
        recipients=["your_email@gmail.com"]
    )

    msg.body = f"Your OTP is {otp}"

    mail.send(msg)

    return "OTP Sent"

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.json

    values = np.array([[
        data["step"],
        encoder.transform([data["type"]])[0],
        data["amount"],
        data["oldbalanceOrg"],
        data["newbalanceOrig"],
        data["oldbalanceDest"],
        data["newbalanceDest"]
    ]])

    pred = model.predict(values)[0]

    result = "Fraud" if pred == 1 else "Safe"

    return jsonify({
        "status": result
    })

@app.route("/bulk_upload", methods=["GET", "POST"])
def bulk_upload():
    if request.method == "POST":
        file = request.files["file"]

        df = pd.read_csv(file)

        if df.empty:
            return render_template("upload.html", error="The uploaded file is empty.")

        df["type"] = encoder.transform(df["type"])

        features = ['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
        
        # Ensure only necessary columns are passed to the model
        preds = model.predict(df[features])

        df["Prediction"] = ["Fraud" if p == 1 else "Safe" for p in preds]

        file_name = "bulk_result.csv"
        df.to_csv(file_name, index=False)

        return send_file(file_name, as_attachment=True)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)