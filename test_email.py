import smtplib

EMAIL    = "psulav679@gmail.com"
PASSWORD = "tlbtzgccqsfuvsux"   # no spaces

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASSWORD)
        s.sendmail(EMAIL, EMAIL, "Subject: Test\n\nIt works!")
        print("✅ Email sent!")
except Exception as e:
    print(f"❌ Error: {e}")