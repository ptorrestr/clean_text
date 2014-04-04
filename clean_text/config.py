import logging

from t2db_objects import objects

from clean_text import data
from clean_text.utilities import formatHash
from clean_text.utilities import readConfigFile
from clean_text.data import confFields
from clean_text.data import confDefault

logger = logging.getLogger()

myConfig = None

def setConfig(confFilePath = None):
  global myConfig
  if confFilePath == None or confFilePath == "":
    logger.warn("No configuration file given, using default confg")
    rawConfigNoFormat = confDefault
  else:
    rawConfigNoFormat = readConfigFile(confFilePath)
  rawConfig = formatHash(rawConfigNoFormat, confFields)
  myConfig = objects.Configuration(confFields, rawConfig)

def getConfig():
  global myConfig
  if myConfig  == None:
    raise Exception("No configuration defined")
  return myConfig
