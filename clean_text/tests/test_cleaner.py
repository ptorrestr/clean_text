import unittest

from os.path import isfile
from os import popen
from os import remove

from clean_text.cleaner import sentenceCleaner
from clean_text.cleaner import tokenCleaner
from clean_text.cleaner import tokenize
from clean_text.cleaner import sentenize
from clean_text.cleaner import cleanSentence
from clean_text.cleaner import Processor 
from clean_text.cleaner import cleaner
from clean_text.config import getConfig
from clean_text.data import setStopwordsPath
from clean_text.globals import init
from clean_text.data import confFields
from clean_text.data import confDefault


""" Count the word in the file given"""
def wordCount(word, file_):
 p = popen("cat " + file_ + " | awk -F '\t' '{print $6}' | grep -w " + word + " | wc -l")
 # Get result and cast it
 pOut = p.read()
 return int(pOut)

class TestCleanerFunctions(unittest.TestCase):
  def setUp(self):
    init()
    setStopwordsPath("./etc/stopwords_en.txt")
    
  def test_sentenceCleaner(self):
    sentence = "this is a @user sample and a http://hi.com sample"
    goldenSentence = "this is a  sample and a  sample"
    self.assertEqual(sentenceCleaner(sentence, ["removeUrl", "removeUserMention"]), goldenSentence)
 
  def test_tokenize(self):
    sentence = "Hello didn't very happy 1313"
    goldenTokens = ["Hello" , "did", "n't", "very", "happy", "1313"]
    tokens = tokenize(sentence)
    for i in range(0, len(tokens)):
      self.assertEqual(tokens[i][0], goldenTokens[i])

  def test_sentenize(self):
    sentence = "Hello I'm very happy 1313"
    goldenSentence = "Hello I 'm very happy 1313"
    tokens = tokenize(sentence)
    self.assertEqual(sentenize(tokens), goldenSentence)
 
  def test_tokenCleaner(self):
    sentence = "Hello I'm very happy 1313"
    goldenSentence = "hello"
    tokens = tokenize(sentence)
    newTokens = tokenCleaner(tokens, ["stemming",
      "removePunctuationAndNumbers", "toLowerCase", "stopwording"])
    self.assertEqual(sentenize(newTokens), goldenSentence)
    
  def test_cleanSentence(self):
    sentence = ("At 8 o'clock on Thursday morning, the boys and " +
      "girls didn't feel very good.")
    sentenceProcList = ["removeUrl", "removeUserMention"]
    tokenProcList = ["stemming", "toLowerCase", "removePunctuationAndNumbers", "stopwording", "removeSingleChar", "removeDoubleChar"]
    newSentence = cleanSentence(sentence, sentenceProcList, tokenProcList)
    goldSentence = "oclock thursday morning boy girl feel good"
    self.assertEqual(newSentence, goldSentence)

  def test_processFile(self):
    rawObject = {
      "date":"Sun Aug 07 01:28:32 IST 2011",
      "id":"100000335933878272",
      "user_id":"71610408",
      "status":"@baloji you were so awesome, it was amazing and you were shining like the star that you are...MERCI!! #baloji i_i"
      }
    goldenRawObject = {
      "date":"Sun Aug 07 01:28:32 IST 2011",
      "id":"100000335933878272",
      "user_id":"71610408",
      "status":"@baloji you were so awesome, it was amazing and you were shining like the star that you are...MERCI!! #baloji i_i",
      "status_clean":"awesome amaze shin star merci baloji"
      }
    rawObjects = [rawObject]
    config = getConfig("", confFields, confDefault)
    proc = Processor(config)
    newRawObject = proc.processFile(rawObjects)
    self.assertEqual(rawObject, goldenRawObject)

  def test_notValidProcessFile(self):
    rawObject = {
      "date":"Sun Aug 07 01:28:32 IST 2011",
      "id":"100000335933878272",
      "user_id":"71610408",
      "status":"@baloji you were so awesome, it was amazing and you were shining like the star that you are...MERCI!! #baloji i_i"
      }
    rawObjects = [rawObject]
    config = getConfig("", confFields, confDefault)
    config.textField = "otherfield"
    proc = Processor(config)
    self.assertRaises(Exception, proc.processFile, rawObjects)

  def test_cleaner(self):
    path = "./etc/example.tsv"
    outputPath = path + ".clean"
    # If file is created, remove it
    if isfile(outputPath):
      remove(outputPath)
    confFilePath = "./etc/example.conf"  
    cleaner(path, outputPath, confFilePath)
    self.assertTrue(isfile(outputPath))
    self.assertEqual(wordCount(" to ", outputPath), 0)
    self.assertEqual(wordCount(" photo ", outputPath), 0)

