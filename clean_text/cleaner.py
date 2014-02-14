import nltk
import sys
import argparse
import logging

from t2db_objects import objects

from clean_text.utilities import formatHash
from clean_text.utilities import readConfigFile
from clean_text import data
from clean_text import globals
from clean_text import setup_logging
from clean_text import functions

# Get log config file

logger = logging.getLogger()

class EmptyOutput(Exception):
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

def mergeHash(tokens):
    mergeTokens = []
    merge = False
    for token in tokens:
        if token[0] == "#" or token[0] == "@":
            merge = True
            save = token[0]
        elif merge:
            newToken = (save + token, token[1])
            mergeTokens.append(newToken)
            merge = False
        else:
            mergeTokens.append(token)
    return mergeTokens

def cleanSentence(sentence, sentenceProcList, tokenProcList):
    # Clean clean
    sentence = sentenceCleaner(sentence, sentenceProcList)
    # Tokenize and pos
    tokens = tokenize(sentence)
    # Clean sentence
    newTokens = tokenCleaner(tokens, tokenProcList)
    # Post clean. Join #, and @
    mergeTokens = mergeHash(newTokens)
    return sentenize(mergeTokens)

""" If the cleanSentence output is empty, the completly line is deleted"""
def processLine(line, sentenceProcList, tokenProcList, criteria = "\t", position = 3, newposition = 4):
    columns = line.split(criteria)
    if position >= len(columns):
        raise Exception("Line only have " + str(len(columns)) + " columns. " + 
            "(Asking for " + str(position) + ", criteriaLine = " + criteria  + " )")
    newStatus = cleanSentence(columns[position], sentenceProcList, tokenProcList)
    if newStatus == "":
        raise EmptyOutput("Original text: " + columns[position] )
    newLine = ""
    # Add the new line in the position given
    if newposition > len(columns):
        raise Exception("New position '" + str(newposition) + "' is not valid (max = " + 
            str(len(columns) + 1) + " )")
    for i in range(0, newposition):
        newLine += columns[i] + criteria
    # Add clean text in this position, with no criteria
    newLine += newStatus
    # if the new position is not the last:
    if not newposition  == len(columns):
        newLine += criteria # add criteria for the next line
        for i in range(newposition, len(columns) - 1):
            newLine += columns[i] + criteria
        #last case
        newLine += columns[len(columns) - 1]
    return newLine

def processFile(fullText, config):
    lines = fullText.split(config.splitCriteriaFile)
    newText = ""
    countLine = 0
    countLineOutput = 0
    for line in lines:
        try:
            countLine += 1
            if line == "":
                logger.warn("Warning: Empty field at line: " + str(countLine))
                continue
            newLine = processLine(line, config.sentenceProcList, 
                config.tokenProcList, config.splitCriteriaLine, 
                config.textColumnPosition, config.newTextColumnPosition)
            newText += newLine + config.splitCriteriaFile
            countLineOutput += 1
        except EmptyOutput as e:
            logger.info("Empty output found at line: " + str(countLine) + ", " + str(e))
        except Exception as e:
            logger.error("Failed at line: " + str(countLine) + ", " + str(e))
            raise
    return [newText, countLine, countLineOutput]

def getConfiguration(confFilePath, confFields, confDefault):
    if confFilePath == "":
        logger.warn("No configuration file given, using default conf")
        rawConfigNoFormat = confDefault
    else:
        rawConfigNoFormat = readConfigFile(confFilePath)
    rawConfig = formatHash(rawConfigNoFormat, confFields)
    config = objects.Configuration(confFields, rawConfig)
    return config
    

def cleaner(path, outputPath, confFilePath):
    globals.init()
    try:        
        config = getConfiguration(confFilePath, globals.confFields, globals.confDefault)
    except Exception as e:
        logger.error("No configuration found")
        raise

    #Set stopwords
    data.setStopwordsPath(config.stopwordFile)
    #Read input file
    with open(path, 'r') as contentFile:
        fullText = contentFile.read()
    [newText, countLine, countLineOutput] = processFile(fullText, config)
    logger.info("Total lines = " + str(countLine) + ", output lines = " + str(countLineOutput))
    with open(outputPath, 'w') as contentFile:
        contentFile.write(newText)

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
        sys.exit(2)
    sys.exit(0)
