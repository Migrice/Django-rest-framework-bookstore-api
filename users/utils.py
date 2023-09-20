import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def send_account_creation_mail( username, email):


    sender_email =  settings.SENDER_EMAIL
    receiver_email = email
    password =  settings.SENDER_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = "Account confirmation"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    user= username
    html = f"""\
    <html>
    <body>
        <p>Hi, {user} <br>
        Your account has been created successfully!<br>
        Welcome to our <a href="https://nextjs-bookstore-app-git-main-migrice.vercel.app">Bookstore</a>
        </p>
    </body>
    </html>
    """

    part2 = MIMEText(html, "html")


    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.MAIL_HOST, 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

