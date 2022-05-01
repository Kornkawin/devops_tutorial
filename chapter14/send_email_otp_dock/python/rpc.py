import smtplib
from email.message import EmailMessage
from nameko.rpc import rpc

def send_email(otp, email):
    msg = EmailMessage()
    text = "OTP สำหรับการลงทะเบียนนักศึกษาใหม่ของท่าน คือ " + str(otp) + ", OTP ของท่านจะหมดอายุใน 2 นาที"
    msg.set_content(text)

    msg['Subject'] = 'Register OTP'
    msg['To'] = email

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login('60f8f73d19e290', '149dab90b40235')
        server.sendmail(from_addr = 'k.bijayayothin@gmail.com', to_addrs = email, msg = msg.as_string())

class Email:
    name = "email_otp"

    @rpc
    def send(self, otp, email):
        send_email(otp, email)
        
