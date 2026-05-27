from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

SENDER_EMAIL    = "psulav679@gmail.com"
SENDER_PASSWORD = "tlbt zgcc qsfu vsux"
RECEIVER_EMAIL  = "psulav679@gmail.com"


def send_email(choice: str):
    subject = "💌 She Forgave You! 🎉" if choice == "yes" else "😤 She Said No... (Angry Bird Mode)"

    if choice == "yes":
        body = "🎉 She clicked YES! She forgave you! Go hug her! 🥰"
    else:
        body = "😬 She clicked NO. Angry bird mode 🐦‍🔥"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg.attach(MIMEText(body, "plain"))

    # port 587 instead of 465
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/respond", methods=["POST"])
def respond():
    data   = request.get_json()
    choice = data.get("choice", "").lower()

    if choice not in ("yes", "no"):
        return jsonify({"status": "error", "message": "Invalid choice"}), 400

    try:
        send_email(choice)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)