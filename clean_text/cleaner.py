"""
=====
cleaner - Highlevel interface
=====
This module encapsultes all the calls necessary to perform cleaning over a collection of data in
a CSV format. The methods here presented can also be used as API directives for cleaning chunks of
string avoiding the CSV format definition. Please ensure have a well-defined configuration file
before used this application
"""

import nltk
import logging

from t2db_objects.serializerXSV import SerializerXSV
from t2db_objects.serializerXSV import BufferedParserXSV
from t2db_objects.utilities import readListFile

from clean_text.utilities import load_stopwords
from clean_text import functions

logger = logging.getLogger("clean_text")

class EmptyOutput(Exception):
  """
  It Controls empyt string output produced by some functions.
  """
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class EmptyInput(Exception):
  """ It Controls empty string input received by some functions. 
  """
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

def sentenceCleaner(sentence, args):
  """ Execute sentence's function list sequentially. The sentence arg contents the initial
      sentence which is used as the input for the first function. Every function will
      received as input argument the output produced by the previous function following
      the sentence's function list definition described on args arg. Note that this function
      is different from the tokenCleaner function. In this case, the sentence ( list of words) 
      are analysed as a whole, rather that to perform word analysis individually.
  """
  tmpSentence = sentence
  for i in range(0, len(args)):
    try:
      tmpSentence = getattr(functions, args[i])(tmpSentence)
    except AttributeError as e:
      raise Exception("Sentence function : '" + args[i] + "' cannot be found")
    if tmpSentence == "":
      break
  return tmpSentence

def tokenize(sentence):
  """ Divide a the sentence arg in one or more substring following the nltk.word_tokenize
      function.
  """
  text = nltk.word_tokenize(sentence)
  return nltk.pos_tag(text)

def sentenize(tokens, space = " "):
  """ Create a string chunk from the list of string given by tokens arg. It uses the space
      arg as the connector among the strings.
  """
  if len(tokens) == 0:
    return ""
  first = True
  sentence = ""
  for i in range(0, len(tokens)):
    if tokens[i][0] != "":
      if first:
        first = False
        sentence = tokens[i][0]
      else:
        sentence += space + tokens[i][0]
  return sentence

def tokenCleaner(tokens, args):
  """ Execute token's function list sequentially. The token arg contents the initial
      token which is used as the input for the first function. Every function will
      received as input, the output produced by the previous function following
      the token's function list definition described on args arg. Note that this function
      is different from the senteceCleaner function. In this case, the tokens(word) are analysed
      individually
  """
  cleanTokens = []
  for token in tokens:
    tmpToken = token
    for i in range(0, len(args)):
      try:
        tmpToken = getattr(functions, args[i])(tmpToken)
      except AttributeError as e:
        raise Exception("Function : '" + args[i] + "' cannot be found")
      if tmpToken[0] == "":
        break
    if not tmpToken[0] == "":
      cleanTokens.append(tmpToken)
  return cleanTokens

def cleanSentence(sentence, sentenceProcList, tokenProcList):
    """ Perform the cleaner sentence procedure. The sentence, the sentence's list function and 
        the token's list function are given by sentece, sentenceProcList and tokenProcList 
        respectivelly. 
        This function first executes the setence's list function, then tokenize the sentence
        and perform the token's list function. If the output is not empty, the function returns it.
        otherwise the EmpytOutput exception is raised.
    """
    if sentence == "":
      raise EmptyInput("Input sentence is empty")
    # Clean clean
    sentence = sentenceCleaner(sentence, sentenceProcList)
    # Tokenize and pos
    tokens = tokenize(sentence)
    # Clean sentence
    newTokens = tokenCleaner(tokens, tokenProcList)
    logger.debug(newTokens)
    # Post clean. 
    newSentence = sentenize(newTokens)
    logger.debug(newSentence)
    if newSentence == "":
      raise EmptyOutput("Output sentence is empty")
    return newSentence

class Processor(object):
  """ Control the cleaning procedure execution over an input file.
  """
  def __init__(self, text_field, new_text_field, sentence_proc_list, token_proc_list): 
    self.countLine = 0
    self.countLineOutput = 0
    self.text_field = text_field
    self.new_text_field = new_text_field
    self.sentence_proc_list = sentence_proc_list
    self.token_proc_list = token_proc_list

  def processFile(self, rawObjects):
    """ It iterates the rawObjects (list) arg and select the appropiate text field 
        declared by the configuration object and execute the cleanSentence function. If the 
        clean text produced an non-empty string, it is stored in the new clean text field 
        declared by the configuration object. The output is the list of newObjects which
        contains the same number of fields plus the new clean text field. This function
        alse returns the number of lines processed and the number of lines generated in
        the outputfile.
    """
    newObjects = []
    for rawObject in rawObjects:
      try:
        self.countLine += 1
        if not self.text_field in rawObject.keys():
          raise Exception("Field '" + self.text_field + "' is not found in object")
        text = rawObject[self.text_field]
        newText = cleanSentence(text, self.sentence_proc_list, self.token_proc_list)
        rawObject[self.new_text_field] = newText
        newObjects.append(rawObject)
        self.countLineOutput += 1
      except EmptyInput as e:
        logger.warn("Empty input found at line: " + str(self.countLine) + ", " + str(e))
      except EmptyOutput as e:
        logger.debug("Empty output found at line: " + str(self.countLine) + ", " + str(e))
      except UnicodeDecodeError as e:
        logger.error("Cannot understant text: " + text + " at line " + str(self.countLine) + ", " + str(e))
        raise
      except Exception as e:
        logger.error("Failed at line: " + str(self.countLine) + ", " + str(e))
        raise
    return [newObjects, self.countLine, self.countLineOutput]

def cleaner(params, config):
  """ This is the core function. First, it sets the configuration file and the stopword file
      then read the input CSV file using a local buffer. The data read is processed line 
      by line and the result is stored in the outpufile.
  """
  #Set stopwords globally
  stopwords = load_stopwords(config.stopword_file_path)
  logger.debug("Configuration = " + str(config.toHash()))
  #Read data from input file
  p = BufferedParserXSV(config.fields, params.input_file, config.buffer_size, config.split_criteria_line)
  s = SerializerXSV(params.output_file, config.over_write_output_file, config.new_fields)
  proc = Processor(config.text_field, config.new_text_field, config.sentence_proc_list, config.token_proc_list)
  while True:
    raw_objects = p.nextObjects()
    if not raw_objects:
      break
    [new_objects, count_line, count_line_output] = proc.processFile(raw_objects)
    logger.info("Lines: Processed = " + str(count_line) + ", Produced = " + str(count_line_output) )
    s.pushObjects(new_objects)
  logger.info("Total lines: Processed = " + str(count_line) + ", Produced = " + str(count_line_output) )

