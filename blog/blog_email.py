import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email_list):
    for email_address in email_list:
        message = MIMEMultipart("alternative")
        message["Subject"] = 'New Post on Philip and Melissa\'s Blog'
        message["From"] = 'philipandmelissalenox@gmail.com'
        message["To"] = email_address.email

        # message to be sent
        text = "Hi Everyone! Thanks for subscribing to Philip and Melissa's Blog. This is a notification that we have a new post. Feel free to check it out at www.philipandmelissalenox.com!!"
        html = "<h3>Hi everyone!</h3><br><p>Thanks for subscribing to Philip and Melissa's Blog. This is a notification that we have a new post. Feel free to check it out at www.philipandmelissalenox.com!!</p>"
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("philipandmelissalenox@gmail.com", "zimllqirqqleynbx")
            server.sendmail(
                "philipandmelissalenox@gmail.com", email_address.email, message.as_string()
            )