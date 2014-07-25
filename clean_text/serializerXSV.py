"""
=====
SerializerXSV
=====
This module controls the methods used to parse, get and store the data stored in CSV or TSV format.
"""

import codecs
import cStringIO
import csv
from itertools import islice
import logging
from os import remove
from os.path import isfile

logger = logging.getLogger("clean_text")

class BufferedReader(object):
  """
  Read a Text file using a buffering aproach. This means that the information is read in chunk of data, 
  one by one, rather than read the whole file. Buffering readings are needed when the XSV file is 
  large.
  """
  def __init__(self, filePath, lines = 100):
    """
    Create a new bufferReader. The filePath points to the file and lines indicates the number of line to
    read in each iteration.
    """
    self.lines = lines
    self.f = codecs.open(filePath, mode = 'r', encoding = 'utf-8')
 
  def close(self):
    """
    Close the file descriptor.
    """
    self.f.close()
 
  def nextLines(self):
    """
    Get the next lines(declared in the constructor) in the file. If there is no more line, a None object
    is returned.
    """
    nextLines = list(islice(self.f, self.lines))
    if not nextLines:
      self.close()
    return nextLines

def append(filePath, lines):
  """
  Add lines to a already existing file. FilePath points to a file. If the file doesn't exist, the function 
  creates it, otherwise the data is added just at the end of the file.
  """
  with codecs.open(filePath, 'a', encoding = 'utf-8') as a:
    a.write(lines)

class Serializer(object):
  """
  The fine a abstract serializer object
  """
  def __init__(self, filePath, overwrite, fields, criteria = '\t'):
    """
    Constructor. FilePath points to the XSV file, overwrite indicates if the file should be rewrite if
    already exist, fields are the list fields which the file should have and critieria is the
    token used to divied fields from other fields.
    """
    self.fields = fields
    self.criteria = criteria
    self.filePath = filePath
    self.overwrite = overwrite
    self.count = 0
    if overwrite and isfile(filePath):
      logger.debug("Overwriting file: " + filePath)
      remove(filePath)

  def serializeLine(self, rawObject):
    """
    Given a object, it create a line (string) which each field following the definition expressed in the
    field attibute. 
    """
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

  def pushObjects(self):
    logger.warn("Not implemented")
    pass


class SerializerXSV(Serializer):
  """
  This class can serialize a XSV file (CSV or TSV)
  """
  def __init__(self, filePath, overwrite,  fields, criteria = "\t"):
    super(SerializerXSV, self).__init__(filePath, overwrite, fields, criteria)

  def pushObjects(self, rawObjectList):
    """
    Store in a file, new objects defined in rawObjectList.
    """
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


class SerializerXSV_CSV(Serializer):
  """
  This class can serialize a XSV file (CSV or TSV)
  """
  def __init__(self, filePath, overwrite,  fields, criteria = "\t"):
    super(SerializerXSV_CSV, self).__init__(filePath, overwrite, fields, criteria)

  def pushObjects(self, rawObjectList):
    lines = []
    for rawObject in rawObjectList:
      lines.append(self.serializeLine(rawObject))
    logger.debug("Objects serialized : " + str(len(rawObjectList)))
    with open(self.filePath, "a") as f:
      UnicodeWriter(f).writerows(lines)

class Parser(object):
  """
  This class can parse a XSV fifle
  """
  def __init__(self, fields, filePath, lines = 100, criteria = "\t"):
    """
    Constructor: The fields contains the list of fields of the XSV file, filePath point to the file, lines
    inidicates the number of line to store in the buffere and criteria is the token defintion to divide
    fields from fields.
    """
    self.fields = fields
    self.reader = BufferedReader(filePath, lines)
    self.criteria = criteria
    self.count = 0

  def close(self):
    """
    Close file descriptior.
    """
    self.reader.close()
    logger.debug("Close reader")

class ParserXSV(Parser):
  """
  This class can parse a XSV fifle
  """
  def parseLine(self, line, lineNum):
    """
    Parse a file line (string) and get a object.
    """
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
    """
    Return the N next objects (genereted from the N next lines).
    """
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

class ParserXSV_CSV(object):
  """
  This class can parse a XSV fifle
  """
  def __init__(self, fields, filePath, lines = 100, criteria = "\t"):
    """
    Constructor: The fields contains the list of fields of the XSV file, filePath point to the file, lines
    inidicates the number of line to store in the buffere and criteria is the token defintion to divide
    fields from fields.
    """
    self.fields = fields
    self.f = open(filePath, "r")
    self.reader = UnicodeReader(self.f, delimiter = criteria, fieldnames = fields)
    self.criteria = criteria
    self.count = 0

  def nextObjects(self):
    """
    Return the all the objects in the file
    """
    rawObjectList = []
    while True:
      item =  self.reader.next()
      if item == None:
        break
      self.count += 1
      rawObjectList.append(item)
    return rawObjectList

  def close(self):
    self.f.close()

# Exceptions
class ColumnsNotEquivalentException(Exception):
  """
  It controls when some object has less or more fields that the XSV file declaration.
  """
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class UTF8Recoder:
  """
  Iterator that reads an encoded stream and reencodes the input to UTF-8
  """
  def __init__(self, f, encoding):
    self.reader = codecs.getreader(encoding)(f)

  def __iter__(self):
    return self

  def next(self):
    n = self.reader.next()
    return n.encode("utf-8")

class UnicodeReader:
  """
  A CSV reader which will iterate over lines in the CSV file "f",
  which is encoded in the given encoding.
  """

  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    f = UTF8Recoder(f, encoding)
    self.reader = csv.DictReader(f, dialect=dialect, **kwds)

  def next(self):
    try:
      row = self.reader.next()
      for elem in row:
        row[elem] = unicode(row[elem], "utf-8")
      return row
    except StopIteration:
      return None

  def __iter__(self):
    return self

class UnicodeWriter:
  """
  A CSV writer which will write rows to CSV file "f",
  which is encoded in the given encoding.
  """

  def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
    # Redirect output to a queue
    self.queue = cStringIO.StringIO()
    self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
    self.stream = f
    self.encoder = codecs.getincrementalencoder(encoding)()

  def writerow(self, row):
    self.writer.writerow([s.encode("utf-8") for s in row])
    # Fetch UTF-8 output from the queue ...
    data = self.queue.getvalue()
    data = data.decode("utf-8")
    # ... and reencode it into the target encoding
    data = self.encoder.encode(data)
    # write to the target stream
    self.stream.write(data)
    # empty queue
    self.queue.truncate(0)

  def writerows(self, rows):
    for row in rows:
      self.writerow(row)
