#!/usr/bin/python
from __future__ import print_function

#import subprocess
import smtplib
#import socket
import datetime
#import sys
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import unittest


def sendMail(attachment):
  try:
    mailto = 'christof.klopp@t-online.de'
    mailfrom = 'Strinzer-Sonnenwerk@t-online.de'
    passw = '$and7m8Spas5'
    smtpserver = smtplib.SMTP('securesmtp.t-online.de', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo

    smtpserver.login(mailfrom, passw)

    date = datetime.date.today()

    msg = MIMEMultipart()
    msg['Subject'] = 'Datenerfassung Strinz ' + attachment
    msg['From'] = mailfrom
    msg['To'] = mailto

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachment, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachement; filename="' + attachment + '"')

    msg.attach(part)

    smtpserver.sendmail(mailfrom, [mailto], msg.as_string())
    smtpserver.quit()
    return True

  except:
    print('Exception in sendMail')
    return False


class TestSendMail(unittest.TestCase):

  def test_send_mail(self):
    sendMail("Test.txt")


