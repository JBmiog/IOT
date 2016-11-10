import smtplib
import email_config

class Emailer():
    server = None

    def __init__(self):
        try:
            self.server = smtplib.SMTP('smtp.gmail.com:587')
        except ConnectionError as err:
            print("cannot connect mail-server", err)

    def tx_email(self, message_data):
        try:
            self.server.ehlo()
            self.server.starttls()
            self.server.login(email_config.username, email_config.password)
            self.server.sendmail(email_config.fromaddr, email_config.toaddrs, message_data)
            self.server.quit()
            return 1
        except ConnectionError as err:
            print("cannot tx email; ", err)
            return 0