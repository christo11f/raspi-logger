#!/usr/bin/python
from __future__ import print_function

import os
import unittest
import mailattach
import storedata


class mailHandler():
 
  directory = storeData.readyToSendDirectory

  def sendPendingMails(self):
    print("Sending pending emails")
    for filename in os.listdir(self.directory):
      print("Try to send: " + filename)
      if mailattach.sendMail(self.directory, filename) == False:
        return False
      else:
        storedata.archiveReadyToSendFile(filename)
        continue
    return True


class TestSendMail(unittest.TestCase):

  def test_send_mails(self):
    mailer = mailHandler()
    mailer.sendPendingMails()




