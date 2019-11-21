import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(receiver_address, mail_subject, mail_content):

    sender_address = 'a0197117y.receiver@gmail.com'
    sender_pass = 'IS5006Receiver'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_subject
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


