#!/usr/bin/python
from __future__ import print_function

from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import ds18b20
import storeData
import logging
import mail

class tempLoggerEmailer:

  retryJob = None
  retryCounter = 0

  def __init__(self):
    logging.basicConfig(filename='temperatureLoggerAndEmailer.log',level=logging.DEBUG)
    logging.info('Main')
    self.scheduler = BlockingScheduler()

    job = self.scheduler.add_job(self.getData, 'cron', second=0)
    job = self.scheduler.add_job(self.sendEmail, 'cron', hour='16', minute=24)

  def getData(self):
    print('Get Data')
    temp = ds18b20.getTemperature()
    print(temp)
    storeData.writeData(temp)

  def sendEmail(self):
    print('Send Email')
    sendSuccessful = mail.sendMail()
    if sendSuccessful == False:
      print('Send mail failed')
      self.retryJob = self.scheduler.add_job(self.retrySendEmail, 'interval', minutes=3)

  def retrySendEmail(self):
    print('Resend Email')
    sendSuccessful = mail.sendMail()
    self.retryCounter = self.retryCounter + 1
    if sendSuccessful == True:
      self.retryJob.remove()
    if self.retryCounter > 2:
      print('Giving up to send email')
      self.retryJob.remove()

  def run(self):
    self.scheduler.start()


def main():
  tempLE = tempLoggerEmailer()
  tempLE.run()

if __name__ == "__main__":
  main()
