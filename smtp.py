# -*- coding: utf-8 -*-
import smtplib
from config import smtp_id, smtp_password, smtp_server, smtp_port
from email.mime.text import MIMEText


def email_myself(msg):

    msg = MIMEText(str(msg))
    me = 'ho1234c@gmail.com'

    msg['Subject'] = 'confirm reservation'
    msg['From'] = me
    msg['To'] = me

    session = smtplib.SMTP(smtp_server, smtp_port)
    session.ehlo()
    session.starttls()

    session.login(smtp_id, smtp_password)
    smtpresult = session.sendmail(me, [me], msg.as_string())
    session.quit()

    if smtpresult:
        return False
    else:
        return True

