import nltk
import sys
import argparse
import logging

from clean_text.config import getConfig
from clean_text.config import setConfig
from clean_text.serializerXSV import ParserXSV
from clean_text.serializerXSV import SerializerXSV
from clean_text import data
from clean_text import dataglobal
from clean_text.logger import setup_logging
from clean_text import functions

# Get log config file

logger = logging.getLogger("clean_text")

class EmptyOutput(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

class EmptyInput(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

def sentenceCleaner(sentence, args):
    tmpSentence = sentence
    for i in range(0, len(args)):
        tmpSentence = getattr(functions, args[i])(tmpSentence)
        if tmpSentence == "":
            break
    return tmpSentence

def tokenize(sentence):
    text = nltk.word_tokenize(sentence)
    return nltk.pos_tag(text)

def sentenize(tokens, space = " "):
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
    if sentence == "":
      raise EmptyInput("Input sentence is empty")
    # Clean clean
    sentence = sentenceCleaner(sentence, sentenceProcList)
    # Tokenize and pos
    tokens = tokenize(sentence)
    # Clean sentence
    newTokens = tokenCleaner(tokens, tokenProcList)
    # Post clean. 
    newSentence = sentenize(newTokens)
    if newSentence == "":
      raise EmptyOutput("Output sentence is empty")
    return newSentence

class Processor(object):
  def __init__(self, config): 
    self.countLine = 0
    self.countLineOutput = 0
    self.config = config

  def processFile(self, rawObjects):
    newObjects = []
    for rawObject in rawObjects:
      try:
        self.countLine += 1
        if not self.config.textField in rawObject.keys():
          raise Exception("Field '" + self.config.textField + "' is not found in object")
        text = rawObject[self.config.textField]
        newText = cleanSentence(text, self.config.sentenceProcList, self.config.tokenProcList)
        rawObject[self.config.newTextField] = newText
        newObjects.append(rawObject)
        self.countLineOutput += 1
      except EmptyInput as e:
        logger.info("Empty input found at line: " + str(self.countLine) + ", " + str(e))
      except EmptyOutput as e:
        logger.info("Empty output found at line: " + str(self.countLine) + ", " + str(e))
      except Exception as e:
        logger.error("Failed at line: " + str(self.countLine) + ", " + str(e))
        raise
    return [newObjects, self.countLine, self.countLineOutput]

def cleaner(path, outputPath, confFilePath):
    dataglobal.init()
    try:
        setConfig(confFilePath)        
        config = getConfig()
    except Exception as e:
        logger.error("No configuration found")
        raise
    #Set stopwords
    data.setStopwordsPath(config.stopwordFile)
    logger.debug("Configuration = " + str(config.toHash()))
    #Read data from input file
    fields = config.fields 
    outFields = config.newFields 
    p = ParserXSV(fields, path, config.bufferSize, config.splitCriteriaLine)
    s = SerializerXSV(outputPath, config.overWriteOutputFile, outFields)
    proc = Processor(config)
    while True:
      rawObjects = p.nextObjects()
      if not rawObjects:
        break
      [newObjects, countLine, countLineOutput] = proc.processFile(rawObjects)
      logger.info("Lines: Processed = " + str(countLine) + ", Produced = " + str(countLineOutput) )
      s.pushObjects(newObjects)
    logger.info("Total lines: Processed = " + str(countLine) + ", Produced = " + str(countLineOutput) )

def main():
    ## Parser input arguments
    parser = argparse.ArgumentParser()
    # positionals
    parser.add_argument('f',
        help='Input file path',
        type = str)
    # with default
    parser.add_argument('-c',
        help = 'Configuration file path',
        default = '',
        type = str,
        required = False)
    parser.add_argument('-o',
        help = 'Output file path',
        default = "./clean.out",
        type = str,
        required = False)
    args = parser.parse_args()
    try:
        setup_logging()
        cleaner(args.f, args.o, args.c)
    except Exception as e:
        logger.error("Error found: " + str(e))
        sys.exit(1)
    sys.exit(0)
