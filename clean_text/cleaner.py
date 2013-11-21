import nltk
from nltk.corpus import wordnet
import re
import sys
import argparse

import logging

from clean_text import data
from clean_text import globals
from clean_text import setup_logging

# Get log config file

logger = logging.getLogger()

class EmptyOutput(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

def removeUrl(sentence):
    urls = re.compile(
        r'(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)', re.IGNORECASE)
    return urls.sub("", sentence)

def removeUserMention(sentence):
    users = re.compile(
        r'@[\w]+')
    return users.sub("", sentence)

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

def setenceCleaner(tokens, args):
    cleanTokens = []
    for token in tokens:
        tmpToken = token
        for i in range(0, len(args)):
            tmpToken = args[i](tmpToken)
            if tmpToken[0] == "":
                break
        if not tmpToken[0] == "":
            cleanTokens.append(tmpToken)
    return cleanTokens

def stemming(token):
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    trans = getWordnetPos(token[1])
    newToken = token[0]
    if not trans == "":
        newToken = lmtzr.lemmatize(newToken, trans)
        if newToken == "n't":
            newToken = "not"
    return (newToken, token[1])

def getWordnetPos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def toLowerCase(token):
    return (token[0].lower(), token[1])

def stopwording(token, language = 'english'):
    if token[0] in nltk.corpus.stopwords.words(language):
        return ("", token[1])
    if token[0] in data.stopwords():
        return ("", token[1])
    return (token[0], token[1])

def removePunctuationAndNumbers(token):
    punctuation = re.compile(r'[\W|0-9|_]')
    return ( punctuation.sub("", token[0]), token[1])

def removeSingleChar(token, excepts = ["#"]):
    if len(token[0]) > 1 or token[0] in excepts:
        return (token[0], token[1])
    return ("", token[1])

def removeDoubleChar(token, excepts = []):
    if len(token[0]) > 2 or token[0] in excepts:
        return (token[0], token[1])
    return ("", token[1])

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

def cleanSentence(sentence):
    # Pre clean
    sentence = removeUrl(sentence)
    sentence = removeUserMention(sentence)
    # Tokenize and pos
    tokens = tokenize(sentence)
    # Clean sentence
    newTokens = setenceCleaner(tokens, [stemming, toLowerCase,
            removePunctuationAndNumbers, stopwording,
            removeSingleChar, removeDoubleChar])

    # Post clean. Join #, and @
    mergeTokens = mergeHash(newTokens)
    return sentenize(mergeTokens)

""" If the cleanSentence output is empty, the completly line is deleted"""
def processLine(line, criteria = "\t", position = 3):
    columns = line.split(criteria)
    if position >= len(columns):
        raise Exception("Line only have " + str(len(columns)) + " columns. " + 
            "(Asking for " + str(position) + ")")
    newStatus = cleanSentence(columns[position])
    if newStatus == "":
        raise EmptyOutput("Original text: " + columns[position] )
    newLine = ""
    for column in columns:
        newLine += column + criteria
    # Add clean text in the end of the line (create a new field)
    newLine += newStatus
    return newLine

def processFile(fullText, criteria = "\n", criteriaForLine = "\t", columnPosition = 4):
    lines = fullText.split(criteria)
    newText = ""
    countLine = 0
    countLineOutput = 0
    for line in lines:
        try:
            if line == "":
                log.debug("Warning: Empty field at line: " + str(countLine))
                continue
            newLine = processLine(line, criteriaForLine, columnPosition)
            newText += newLine + criteria
            countLineOutput += 1
        except EmptyOutput as e:
            logger.info("Empty output found at line: " + str(countLine) + ", " + str(e))
        except Exception as e:
            logger.error("Failed at line: " + str(countLine) + ", " + str(e))
            raise
        countLine += 1
    return [newText, countLine, countLineOutput]

def cleaner(path, outputPath, stopwordsPath, criteriaForFile = "\n", 
        criteriaForLine = "\t", columnPosition = 4):
    globals.init()
    #Set stopwords
    data.setStopwordsPath(stopwordsPath)
    #Read input file
    with open(path, 'r') as contentFile:
        fullText = contentFile.read()
    [newText, countLine, countLineOutput] = processFile(fullText, 
        criteriaForFile, criteriaForLine, columnPosition)
    logger.info("Total lines = " + str(countLine) + ", output lines = " + str(countLineOutput))
    with open(outputPath, 'w') as contentFile:
        contentFile.write(newText)

def main():
    ## Parser input arguments
    parser = argparse.ArgumentParser()
    # positionals
    parser.add_argument('-f',
        help='Input file path',
        type = str,
        required = True)
    # with default
    parser.add_argument('-o',
        help = 'Output file path',
        default = "./clean.out",
        type = str,
        required = False)
    parser.add_argument('-cf',
        help = 'Split criteria for file, default = newline',
        default = "\n",
        type = str,
        required = False)
    parser.add_argument('-cl',
        help = 'Split criteria for line, default = tab',
        default = "\t",
        type = str,
        required = False)
    parser.add_argument('-cp',
        help = 'Text column position in file',
        default = 3,
        type = int,
        required = False)
    parser.add_argument('-sw',
        help = 'Stopword file, default = None',
        default = '',
        type = str,
        required = False)
    args = parser.parse_args()
    try:
        setup_logging()
        cleaner(args.f, args.o, args.sw, args.cf, args.cl, args.cp)
    except Exception as e:
        logger.error("Error found: " + str(e))
        logger.shutdown()
        sys.exit(2)
    logger.shutdown()
    sys.exit(0)
