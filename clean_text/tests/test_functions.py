import unittest

from clean_text.functions import removeUrl
from clean_text.functions import removeUserMention
from clean_text.functions import stemming
from clean_text.functions import stopwording
from clean_text.functions import toLowerCase
from clean_text.functions import removePunctuationAndNumbers
from clean_text.functions import removeSingleChar
from clean_text.functions import removeDoubleChar

from clean_text.cleaner import tokenize
from clean_text.cleaner import sentenize
from clean_text.data import setStopwordsPath
from clean_text.dataglobal import init

class TestFunctionsFunctions(unittest.TestCase):
  def setUp(self):
    init()
    setStopwordsPath("./etc/stopwords_en.txt")

  def test_removeUrl(self):
    sentence = "this is an URL http://google.ie http://google.cl http://google.com"
    goldenSentence = "this is an URL   "
    self.assertEqual(removeUrl(sentence), goldenSentence)

  def test_removeUserMention(self):
    sentence = "this is an user @ptorrestr @asa23"
    goldenSentence = "this is an user  "
    self.assertEqual(removeUserMention(sentence), goldenSentence)

  def test_stemming(self):
    sentence = "boys and women want to have homes, not cars going and archives"
    goldenSentence = "boy and woman want to have home , not car go and archive"
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(stemming(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)

  def test_toLowerCase(self):
    sentence = "bOys WOMEN Homes MeN cARs aRchIvES"
    goldenSentence = "boys women homes men cars archives"
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(toLowerCase(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)

  def test_stopwording(self):
    sentence = "at eight not on thursday morning Arthur didn't feel very good"
    goldenSentence = "eight thursday morning Arthur n't feel good"
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(stopwording(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)

  def test_removePunctuationAndNumbers(self):
    sentence = "at 8 o'clock on (thursday) morning Arthur didn't feel very good."
    goldenSentence = "at oclock on thursday morning Arthur did nt feel very good"
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(removePunctuationAndNumbers(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)

  def test_removeSingleChar(self):
    sentence = "at 8 o'clock on (Thursday) morning Arthur didn't feel very good."
    goldenSentence = "at o'clock on Thursday morning Arthur did n't feel very good"
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(removeSingleChar(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)

  def test_removeDoubleChar(self):
    sentence = "at 8 o'clock on (Thursday) morning Arthur didn't feel very good."
    goldenSentence = "8 o'clock ( Thursday ) morning Arthur did n't feel very good ."
    tokens = tokenize(sentence)
    newTokens = []
    for token in tokens:
      newTokens.append(removeDoubleChar(token))
    self.assertEqual(sentenize(newTokens), goldenSentence)
