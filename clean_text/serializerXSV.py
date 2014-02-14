from itertools import islice
import logging

logger = logging.getLogger()

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
  def __init__(self, filePath, fields, criteria = "\t"):
    self.fields = fields
    self.criteria = criteria
    self.filePath = filePath
    self.count = 0 

  def serializeLine(self, rawObject):
    columns = []
    if not len(self.fields) == len(rawObject.keys()):
      raise ColumnsNotEquivalentException("Column and fields missmatch")
    for field in self.fields:
      try:
        columns.append(rawObject[field])
      except Exception as e:
        raise ColumnsNotEquivalentException("Field missing: " + field)
    line = columns[0]
    for i in range(1, len(columns)):
      line += self.criteria + columns[i]
    return line

  def pushObjects(self, rawObjectList):
    lines = []
    for rawObject in rawObjectList:
      lines.append(self.serializeLine(rawObject))
      self.count += self.count
    contentFile = lines[0]
    for i in range(1, len(lines)):
      contentFile += "\n" + lines[i]
    append(self.filePath, contentFile)
     

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
 
  def parseLine(self, line, lineNum):
    columns = line.split(self.criteria)
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
    return rawObjectList

# Exceptions
class ColumnsNotEquivalentException(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)
