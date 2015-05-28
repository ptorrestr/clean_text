"""
=====
Utilities
=====
"""
import logging

from t2db_objects.utilities import readListFile

logger = logging.getLogger("clean_text")

class NotWellFormedException(Exception):
  """
  It controls the configuration file structure. When some element of the configuration structure (defined 
  in data.py) is missing, this Exception will be raised.
  """
  def __init__(self, value):
    self.value = value
  
  def __str__(self):
    return repr(self.value)

def load_stopwords(stopwords_file_path):
  """
  Get a list of stopword defined in the stopword file path.
  """
  # load stopwords
  stopwords = []
  try:
    stopwords = readListFile(stopwords_file_path)
  except Exception as e:
   logger.warn("Couldn't read stopword file: " + stopwords_file_path)
  return stopwords
