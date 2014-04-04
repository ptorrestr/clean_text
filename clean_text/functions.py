"""
=====
Functions - Token's and sentence's function declarations.
=====
This file has the basic function for cleaning. The functions are divided
in two categories, sentences and tokens.
Sentences functions explore the entire sentence (string) without tokenise
the string. In the other hand, tokens functions analyse the sentence dividing
the string first.
"""
import nltk
from nltk.corpus import wordnet
import re
import logging

from clean_text import data

logger = logging.getLogger("clean_text")

def removeUrl(sentence):
  """
  Sentence function
  Input: The sentence string (list of token).
  Remove URLs
  """
  #TODO: Improve URL pattern
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
  """
  Sentence function
  Input: The sentence string (list of token).
  Remove twitter user mention (@something)
  """
  users = re.compile(
    r'@[\w]+')
  return users.sub("", sentence)

def stemming(token):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Get the root of the word.
  """
  lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
  trans = getWordnetPos(token[1])
  newToken = token[0]
  if not trans == "":
    newToken = lmtzr.lemmatize(newToken, trans)
    if newToken == "n't":
      newToken = "not"
  return (newToken, token[1])

def getWordnetPos(tag):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Utilitary function. Get the tag of the word,
  """
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
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming). 
  Transform upper case to lower case.
  """
  #TODO: can be applied direclty to the sentence?
  return (token[0].lower(), token[1])

def stopwording(token, language = 'english'):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Determine if the word is stopword or not.
  """
  #TODO: Use a better data-structure. Other languages
  if token[0] in nltk.corpus.stopwords.words(language):
    return ("", token[1])
  if token[0] in data.stopwords():
    return ("", token[1])
  return (token[0], token[1])

def removePunctuationAndNumbers(token):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Eliminate punctuation chars and numbers (digits)
  """
  #TODO: Can be applied directly to the sentence?
  punctuation = re.compile(r'[\W|0-9|_]')
  return ( punctuation.sub("", token[0]), token[1])

def removeSingleChar(token, excepts = ["#"]):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Eliminate string that is composed by 1 char only.
  """
  if len(token[0]) > 1 or token[0] in excepts:
    return (token[0], token[1])
  return ("", token[1])

def removeDoubleChar(token, excepts = []):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Eliminate strings that are composed by 2 char only.
  """
  lengthToken = len(token[0])
  if lengthToken == 2 and token[0] not in excepts:
    return ("", token[1])
  return (token[0], token[1])

def mergeHash(tokens):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  The tokinize function usually divide hashtagas and twiiter user description. This function
  reconnect hashtag description and twitter user name (Not in used).
  """
  # Determine if is necesary? Unittest missing.
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
