import nltk
import re
import sys
import argparse

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
    return nltk.word_tokenize(sentence)

def sentenize(tokens, space = " "):
    if len(tokens) == 0:
        return ""
    sentence = ""
    for i in range(0, len(tokens)-1):
        sentence += tokens[i] + space
    return sentence + tokens[len(tokens) - 1 ]

def setenceCleaner(tokens, args):
    cleanTokens = []
    for token in tokens:
        tmpToken = token
        for i in range(0, len(args)):
            tmpToken = args[i](tmpToken)
            if tmpToken == "":
                break
        if not tmpToken == "":
            cleanTokens.append(tmpToken)
    return cleanTokens

def stemming(token):
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    newToken = lmtzr.lemmatize(token)
    if newToken == "n't":
        newToken = "not"
    return newToken

def toLowerCase(token):
    return token.lower()

def stopwording(token, language = 'english'):
    if not token in nltk.corpus.stopwords.words(language):
        return token
    return ""

def removePunctuationAndNumbers(token):
    punctuation = re.compile(r'[\W|0-9|_]')
    return punctuation.sub("", token)

def removeSingleChar(token, excepts = ["#"]):
    if len(token) > 1 or token in excepts:
        return token
    return ""

def removeDoubleChar(token, excepts = []):
    if len(token) > 2 or token in excepts:
        return token
    return ""

def mergeHash(tokens):
    mergeTokens = []
    merge = False
    for token in tokens:
        if token == "#" or token == "@":
            merge = True
            save = token
        elif merge:
            mergeTokens.append(save + token)
            merge = False
        else:
            mergeTokens.append(token)
    return mergeTokens

def cleanSentence(sentence):
    # Pre clean
    sentence = removeUrl(sentence)
    sentence = removeUserMention(sentence)
    # Tokenize
    tokens = tokenize(sentence)
    # Clean sentence
    newTokens = setenceCleaner(tokens, [stemming, toLowerCase,
            removePunctuationAndNumbers, stopwording,
            removeSingleChar, removeDoubleChar])

    # Post clean. Join #, and @
    mergeTokens = mergeHash(newTokens)
    return sentenize(mergeTokens)

def processLine(line, criteria = "\t", position = 3):
    columns = line.split(criteria)
    if position >= len(columns):
        raise Exception("Line only have " + str(len(columns)) + " columns. " + 
            "(Asking for " + str(position) + ")")
    newTweet = cleanSentence(columns[position])
    columns[position] = newTweet
    newLine = ""
    for column in columns:
        newLine += column + criteria
    return newLine

def processFile(fullText, criteria = "\n", criteriaForLine = "\t", columnPosition = 3):
    lines = fullText.split(criteria)
    newText = ""
    countLine = 0
    for line in lines:
        try:
            if line == "":
                print("Warning: Empty line at line: " + str(countLine))
                continue
            newLine = processLine(line, criteriaForLine, columnPosition)
            newText += newLine + criteria
        except Exception as e:
            print("Failed at line: " + str(countLine) + ", " + str(e))
            raise
        countLine += 1
    return newText

def cleaner(path, outputPath, criteriaForFile = "\n", criteriaForLine = "\t",
        columnPosition = 3):
    with open(path, 'r') as contentFile:
        fullText = contentFile.read()
    newText = processFile(fullText, criteriaForFile, criteriaForLine, columnPosition)
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
    args = parser.parse_args()
    try:
        cleaner(args.f, args.o, args.cf, args.cl, args.cp)
    except Exception as e:
        print("Error found: " + str(e))
        sys.exit(2)
    sys.exit(0)
