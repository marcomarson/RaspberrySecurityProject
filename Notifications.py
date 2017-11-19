import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendemail(emailaddr):
    fromaddr = "mam.uepg2017@gmail.com"
    toaddr = emailaddr

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Portão aberto"

    body = "portão aberto por muito tempo"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "password") # mudar para a senha original
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
