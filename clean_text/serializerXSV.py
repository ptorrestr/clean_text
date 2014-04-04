from itertools import islice
import logging
from os import remove
from os.path import isfile

logger = logging.getLogger("clean_text")

class BufferedReader(object):
  def __init__(self, filePath, lines = 100):
    self.lines = lines
    self.f = open(filePath, 'r')
 
  def close(self):
    self.f.close()
 
  def nextLines(self):
    nextLines = list(islice(self.f, self.lines))
    if not nextLines:
      self.close()
    return nextLines

def append(filePath, lines):
  with open(filePath, 'a') as a:
    a.write(lines)

class Serializer(object):
  pass

class SerializerXSV(Serializer): 
  def __init__(self, filePath, overwrite,  fields, criteria = "\t"):
    self.fields = fields
    self.criteria = criteria
    self.filePath = filePath
    self.overwrite = overwrite
    self.count = 0
    if overwrite and isfile(filePath):
      logger.debug("Overwriting file: " + filePath)
      remove(filePath)

  def serializeLine(self, rawObject):
    columns = []
    for field in self.fields:
      try:
        columns.append(rawObject[field])
      except Exception as e:
        raise ColumnsNotEquivalentException("Field missing: " + field + " obj = " + str(rawObject))
    line = columns[0]
    for i in range(1, len(columns)):
      line += self.criteria + columns[i]
    return line

  def pushObjects(self, rawObjectList):
    lines = []
    for rawObject in rawObjectList:
      lines.append(self.serializeLine(rawObject))      
    logger.debug("Objects serialized : " + str(len(rawObjectList)))
    #If they are already data before, add a new line
    if self.count == 0 and self.overwrite:
      contentFile = lines[0]
    else:
      contentFile = "\n" + lines[0]
    for i in range(1, len(lines)):
      contentFile += "\n" + lines[i]
    append(self.filePath, contentFile)
    self.count += len(lines)
    logger.debug("Current lines output : " + str(self.count))
     

class Parser(object):
  pass

class ParserXSV(Parser):
  def __init__(self, fields, filePath, lines = 100, criteria = "\t"):
    self.fields = fields
    self.reader = BufferedReader(filePath, lines)
    self.criteria = criteria
    self.count = 0

  def close(self):
    self.reader.close()
    logger.debug("Close reader")
 
  def parseLine(self, line, lineNum):
    columns = line.strip().split(self.criteria)
    if len(self.fields) > len(columns):
      raise ColumnsNotEquivalentException("Line " + str(lineNum) + ": Column missing, fields = " 
        + str(len(self.fields)) + ", columns = " + str(len(columns)))
    if len(self.fields) < len(columns):
      logger.warn("Line " + str(lineNum) + ": Some columns are not considered")
    rawObject = {}
    i = 0
    for field in self.fields:
      rawObject[field] = columns[i]
      i += 1
    return rawObject

  def nextObjects(self):
    lines = self.reader.nextLines()
    if not lines:
      return lines
    rawObjectList = []
    for line in lines:
      self.count += 1
      if line == "":
        logger.warn("Empty line found at: " + str(countLine))
      rawObject = self.parseLine(line, self.count)
      rawObjectList.append(rawObject)
    logger.debug("Objects read = " + str(len(rawObjectList)))
    return rawObjectList

# Exceptions
class ColumnsNotEquivalentException(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)
