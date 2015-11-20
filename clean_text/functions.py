# -*- coding: utf-8 -*-
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
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown
from nltk.corpus import wordnet
from nltk.corpus import stopwords as nltk_stopwords
import re
import logging

from clean_text.language import get_languages
from clean_text.language import recognize_language

logger = logging.getLogger("clean_text")

stopwords = []

# URL patter. Obtained from https://gist.github.com/gruber/249502
# Multi-line commented version of same pattern:
url_pattern = re.compile(
  r'(?xi)'
  r'\b'
  r'(' # Capture 1: entire matched URL
  r'(?:'
  r'[a-z][\w-]+:' # URL protocol and colon
  r'(?:'
  r'/{1,3}' # 1-3 slashes
  r'|' # or
  r'[a-z0-9%]' # Single letter or digit or '%'
  # (Trying not to match e.g. "URI::Escape")
  r')'
  r'|' # or
  r'www\d{0,3}[.]' # "www.", "www1.", "www2." … "www999."
  r'|' # or
  r'[a-z0-9.\-]+[.][a-z]{2,4}/' # looks like domain name followed by a slash
  r')'
  r'(?:' # One or more:
  r'[^\s()<>]+' # Run of non-space, non-()<>
  r'|' # or
  r'\(([^\s()<>]+|(\([^\s()<>]+\)))*\)' # balanced parens, up to 2 levels
  r')+'
  r'(?:' # End with:
  r'\(([^\s()<>]+|(\([^\s()<>]+\)))*\)' # balanced parens, up to 2 levels
  r'|' # or
  r'[^\s`!()\[\]{};:\'".,<>?«»“”‘’]' # not a space or one of these punct char
  r')'
  r')'
  )

def removeUrl(sentence):
  """
  Sentence function
  Input: The sentence string (list of token).
  Remove URLs
  """
  return url_pattern.sub("", sentence)

def removeUserMention(sentence):
  """
  Sentence function
  Input: The sentence string (list of token).
  Remove twitter user mention (@something)
  """
  users = re.compile(
    r'@[\w]+')
  return users.sub("", sentence)

def englishLanguage(sentence):
  """
  Sentence function
  Input: The sentence string
  If the sentence language is english, the function will return a non-empty string. Otherwise, an empty string will be returned.
  Output: String
  """
  my_lang = recognize_language(sentence, get_languages(), threshold = 0.85)
  if my_lang and my_lang.name == 'english':
    return sentence
  return ''

def stemming(token):
  """
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Get the root of the word.
  """
  lmtzr = WordNetLemmatizer()
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
  #global stopwords
  #TODO: Use a better data-structure. Other languages
  lang_stopwords = set(nltk_stopwords.words(language))
  if token[0] in lang_stopwords:
    return ("", token[1])
  if token[0] in stopwords:
    return ("", token[1])
  return (token[0], token[1])


def removePunctuationAndNumbers(token):
  """  
  Token functions
  Input: two-length list. The first element is the word, and the sencond the tag(stemming).
  Eliminate punctuation chars and numbers (digits)
  """
  punctuation = re.compile(r'[\W|0-9|_]', re.UNICODE)
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
