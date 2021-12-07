from flask import Flask, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from getpass import getpass

app = Flask(__name__)

sender = None
password = None


@app.route("/", methods=["POST", "GET"])
def server():
    msg = MIMEMultipart()
    msg["Subject"] = request.form["subject"]
    msg["From"] = sender
    msg["To"] = request.form["to"]
    body_text = request.form["body"]
    body_part = MIMEText(body_text, 'html')

    for filename in request.files:
        part = MIMEApplication(request.files[filename].stream.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    msg.attach(body_part)
    with smtplib.SMTP(host="smtp.titan.email", port=587) as smtp_obj:
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.ehlo()
        smtp_obj.login(msg["From"], password)
        smtp_obj.sendmail(msg['From'], [msg['To'], ], msg.as_string())
    return "DONE"


def run():
    global sender
    global password
    sender = input("Sender Email: ")
    password = getpass("Password: ")
    app.run(port=5000)
