email_config.server.ehlo()
def tx_email(message_data):
    email_config.server.starttls()
    email_config.server.login(email_config.username, email_config.password)
    email_config.server.sendmail(email_config.fromaddr, email_config.toaddrs, message_data)
    email_config.server.quit()
