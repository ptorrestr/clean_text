import logging

from t2db_objects import objects

from clean_text import data
from clean_text.utilities import formatHash
from clean_text.utilities import readConfigFile

logger = logging.getLogger()

def getConfig(confFilePath, confFields, confDefault):
  if confFilePath == "":
    logger.warn("No configuration file given, using default conf")
    rawConfigNoFormat = confDefault
  else:
    rawConfigNoFormat = readConfigFile(confFilePath)
  rawConfig = formatHash(rawConfigNoFormat, confFields)
  config = objects.Configuration(confFields, rawConfig)
  return config
