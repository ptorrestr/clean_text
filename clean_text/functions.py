import nltk
from nltk.corpus import wordnet
import re

from clean_text import data

#This file has the basic function for cleaning. The functions are divided
#in two categories, sentences and tokens. 
# Sentences functions explore the entire sentence (string) without tokenise
#the string. In the other hand, tokens functions analyse the sentence dividing
#the string first.

# Sentence functions
# Input: The sentence string.
##################################################################################
def removeUrl(sentence):
  #TODO: Improve URL pattern
  """ Remove Urls from sentence"""
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
  """ Remove user mention (@something)"""
  users = re.compile(
    r'@[\w]+')
  return users.sub("", sentence)

# Token functions
# Input: two-length list. The first element is the word, and the sencond the tag(stemming)
#########################################################################################
def stemming(token):
  """ Get the root of the word """
  lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
  trans = getWordnetPos(token[1])
  newToken = token[0]
  if not trans == "":
    newToken = lmtzr.lemmatize(newToken, trans)
    if newToken == "n't":
      newToken = "not"
  return (newToken, token[1])

def getWordnetPos(tag):
  """ Utilitary function. Get the tag of the word """
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
  #TODO: can be applied direclty to the sentence?
  """ Transform upper case to lower case """
  return (token[0].lower(), token[1])

def stopwording(token, language = 'english'):
  #TODO: Use a better data-structure. Other languages
  """ Determine if the word is stop or not """
  if token[0] in nltk.corpus.stopwords.words(language):
    return ("", token[1])
  if token[0] in data.stopwords():
    return ("", token[1])
  return (token[0], token[1])

def removePunctuationAndNumbers(token):
  #TODO: Can be applied directly to the sentence?
  """ Eliminate punctuation chars and numbers (digits) """
  punctuation = re.compile(r'[\W|0-9|_]')
  return ( punctuation.sub("", token[0]), token[1])

def removeSingleChar(token, excepts = ["#"]):
  """ Eliminate string that is composed by 1 char only """
  if len(token[0]) > 1 or token[0] in excepts:
    return (token[0], token[1])
  return ("", token[1])

def removeDoubleChar(token, excepts = []):
  """ Eliminate strings that are composed by 2 char only """
  lengthToken = len(token[0])
  if lengthToken == 2 and token[0] not in excepts:
    return ("", token[1])
  return (token[0], token[1])
