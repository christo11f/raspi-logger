#!/usr/bin/python
from __future__ import print_function

from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import ds18b20
import storedata
import logging
from mailhandler import mailHandler
import os

class tempLoggerEmailer:

  retryJob = None
  retryCounter = 0
  mailer = mailHandler()

  def __init__(self):
    storedata.initPaths()
    logging.basicConfig(filename='temperatureLoggerAndEmailer.log',level=logging.DEBUG)
    logging.info('Main')
    self.scheduler = BlockingScheduler()

    job = self.scheduler.add_job(self.getData, 'cron', minute='0,10,20,30,40,50')
    job = self.scheduler.add_job(self.sendEmail, 'cron', hour='00', minute=10)

  def getData(self):
    print('Get Data')
    temp = ds18b20.getTemperature()
    print(temp)
    storedata.writeData(temp)

  def sendEmail(self):
    print('Send Email')
    sendSuccessful = self.mailer.sendPendingMails()
    if sendSuccessful == False:
      print('Send mail failed')
      self.retryJob = self.scheduler.add_job(self.retrySendEmail, 'interval', minutes=3)

  def retrySendEmail(self):
    print('Resend Email')
    sendSuccessful = self.mailer.sendPendingMails()
    self.retryCounter = self.retryCounter + 1
    if sendSuccessful == True:
      self.retryJob.remove()
    if self.retryCounter > 2:
      print('Giving up to send email')
      self.retryJob.remove()

  def run(self):
    print('Run the logger and mailer')
    self.sendEmail()
    self.scheduler.start()


def main():
  print("Working dir: " + os.getcwd())
  filedir = os.path.dirname(os.path.abspath(__file__))
  os.chdir(filedir)
  print("New working dir: " + os.getcwd())
  tempLE = tempLoggerEmailer()
  tempLE.run()

if __name__ == "__main__":
  main()
