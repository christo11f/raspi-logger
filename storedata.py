#!/usr/bin/python
import time
import os
import unittest
import shutil

currentDirectory = "current"
archiveDirectory = "archive"
readyToSendDirectory = "ready-to-send"

def writeData(TempAsFloat):
  filename = time.strftime("%Y%m%d.csv")
  filenameWithPath = os.path.join(currentDirectory, filename)
  print(filenameWithPath)
  try:
    file = open(filenameWithPath,"a")
    file.write(time.strftime("%d.%m.%Y, %H:%M:%S"))
    file.write(", %.1f \n" % TempAsFloat)
    file.close() 
  except IOError:
    print("could not write file")
  moveOldFiles(filename)

def moveOldFiles(currentFileName):
  for filename in os.listdir(currentDirectory):
    if filename == currentFileName:
      print("found current file")
      continue
    else:
      print("found old file "+filename)
      sourceFile = os.path.join(currentDirectory, filename)
      destinationFile = os.path.join(readyToSendDirectory, filename)
      shutil.move(sourceFile, destinationFile)
      continue

def archiveReadyToSendFile(filename):
  sourceFile = os.path.join(readyToSendDirectory, filename)
  destinationFile = os.path.join(archiveDirectory, filename)
  shutil.move(sourceFile, destinationFile)  

def initPaths():
  if not os.path.exists(currentDirectory):
    os.makedirs(currentDirectory)

  if not os.path.exists(archiveDirectory):
    os.makedirs(archiveDirectory)

  if not os.path.exists(readyToSendDirectory):
    os.makedirs(readyToSendDirectory)  


class TestStoreData(unittest.TestCase):

  def test_write_data(self):
    writeData(100)

  def test_init_paths(self):
    initPaths()

  def test_check_old_files(self):
    moveOldFiles("Hallo.csv")
