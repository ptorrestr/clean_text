"""
=====
Utilities
=====
"""
import logging

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


def readConfigFile(configFilePath):
  """
  Read the file pointed by configFilePath and create a dictionary with the information. If a line
  of the file starts with the simbol '#', then the line is considered a comment.
  """
  properties = {}
  numLine = 1
  with open(configFilePath, "r", -1) as configFile:
    for line in configFile:
      if not line.startswith("#") and len(line.strip()) > 0:
        terms = line.strip().split("=")
        try:
          # If \t or \n are in the file, they are considere the special symbols for tab and new line respectively
          key = terms[0].strip()
          value = terms[1].strip()
          if value == "\\t":
            value = "\t"
          elif value == "\\n":
            value = "\n"
          properties[key] = value
        except Exception as e:
          raise NotWellFormedException("File not well formed, line: " + str(numLine))
      numLine += 1
  return properties

def formatHash(myHash, myFields):
  """
  Ensure that the configuration values (myHash) are in the correct format (myFields).
  """
  newHash = {}
  for field in myFields:
    if not "name" in field:
      raise Exception ("'" + field + "' is not valid tuple: Name missing")
    if not "kind" in field:
      raise Exception ("'" + field + "' is not valid tuple: Kind missing")
    if not "type" in field:
      raise Exception ("'" + field + "' is not valid tuple: Type missing")
    name_ = field["name"]
    kind_ = field["kind"]
    type_ = field["type"]
    if kind_ == "mandatory" and not name_ in myHash:
      raise Exception ("'Object does not have '" + name_ + "'")
    if name_ in myHash:
      if type_ == list:
        newHash[name_] = myHash[name_].split()
      else:
        newHash[name_] = type_(myHash[name_])
  return newHash
