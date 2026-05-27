from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# ── Email config ── put your Gmail + App Password here ──
SENDER_EMAIL    = "psulav679@gmail.com"       # your Gmail
SENDER_PASSWORD = "tlbt zgcc qsfu vsux"     # Gmail App Password (not your real password)
RECEIVER_EMAIL  = "psulav679@gmail.com"       # where YOU receive the notification


def send_email(choice: str):
    subject = "💌 She Forgave You! 🎉" if choice == "yes" else "😤 She Said No... (Angry Bird Mode)"

    if choice == "yes":
        body = """
        🎉 GREAT NEWS! 🎉

        She clicked YES! She forgave you! 💕

        Go give her a hug right now! 🥰
        """
    else:
        body = """
        😬 Uh oh...

        She clicked NO. Angry bird mode activated 🐦‍🔥

        Maybe try flowers? Or more apologies? 😅
        """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
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
        # still return ok so the frontend works even if email fails
        return jsonify({"status": "ok", "warning": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
