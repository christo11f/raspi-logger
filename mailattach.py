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
import os
import private


def sendMail(directory, attachment):
  attachmentWithPath = os.path.join(directory, attachment)
  try:
    smtpserver = smtplib.SMTP('securesmtp.t-online.de', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo

    smtpserver.login(private.mailfrom, private.passw)

    date = datetime.date.today()

    msg = MIMEMultipart()
    msg['Subject'] = 'Datenerfassung Strinz ' + attachment
    msg['From'] = private.mailfrom
    msg['To'] = private.mailto

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(attachmentWithPath, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachement; filename="' + attachment + '"')

    msg.attach(part)

    smtpserver.sendmail(private.mailfrom, [private.mailto], msg.as_string())
    smtpserver.quit()
    return True

  except Exception as e:
    print('Exception in sendMail: ' + str(e))
    return False


class TestSendMail(unittest.TestCase):

  def test_send_mail(self):
    sendMail("Test.txt")


