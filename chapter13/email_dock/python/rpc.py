import smtplib
from email.message import EmailMessage
from nameko.rpc import rpc

def send(id, firstname, lastname, email):
    msg = EmailMessage()
    text = "สวัสดีครับ คุณ " + firstname + " " + lastname + " รหัสนักศึกษา " + str(id) + " ได้ลงทะเบียนแล้ว"
    msg.set_content(text)

    msg['Subject'] = 'Register complete'
    msg['To'] = email

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login('60f8f73d19e290', '149dab90b40235')
        server.sendmail(from_addr = 'k.bijayayothin@gmail.com', to_addrs = email, msg = msg.as_string())

class Email:
    name = "email"

    @rpc
    def send(self, id, firstname, lastname, email):
        send(id, firstname, lastname, email)
