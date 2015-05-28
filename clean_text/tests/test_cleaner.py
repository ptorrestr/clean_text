# -*- coding: utf-8 -*-

import unittest
import logging

from os.path import isfile
from os import popen
from os import remove

from t2db_objects import objects
from t2db_objects.utilities import formatHash
from t2db_objects.parameters import generate_config

from clean_text.cleaner import sentenceCleaner
from clean_text.cleaner import tokenCleaner
from clean_text.cleaner import tokenize
from clean_text.cleaner import sentenize
from clean_text.cleaner import cleanSentence
from clean_text.cleaner import Processor 
from clean_text.cleaner import cleaner
from clean_text.utilities import load_stopwords
from clean_text.run import param_fields
from clean_text.run import conf_fields
from clean_text import functions

logger = logging.getLogger('clean_text')

""" Count the word in the file given"""
def wordCount(word, file_):
 p = popen("cat " + file_ + " | awk -F '\t' '{print $6}' | grep -w " + word + " | wc -l")
 # Get result and cast it
 pOut = p.read()
 p.close()
 return int(pOut)

class TestCleanerFunctions(unittest.TestCase):
  def setUp(self):
    pass
 
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
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    newTokens = tokenCleaner(tokens, ["stemming", "toLowerCase", "removePunctuationAndNumbers", "stopwording"])
    self.assertEqual(sentenize(newTokens), goldenSentence)
    
  def test_cleanSentence(self):
    sentence = ("At 8 o'clock on Thursday morning, the boys and girls didn't feel very good.")
    sentenceProcList = ["removeUrl", "removeUserMention"]
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    tokenProcList = ["stemming", "toLowerCase", "removePunctuationAndNumbers", "stopwording", "removeSingleChar", "removeDoubleChar"]
    newSentence = cleanSentence(sentence, sentenceProcList, tokenProcList)
    goldSentence = "oclock thursday morning boy girl feel good"
    self.assertEqual(newSentence, goldSentence)

  def test_cleanSentenceUnicode(self):
    sentence = u"Según @NWS_PTWC, no hay riesgo generalizado de #tsunami tras el #sismo de Japón http://t.co/icErcNfSCf"
    sentenceProcList = ["removeUrl", "removeUserMention"]
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    tokenProcList = ["stemming", "toLowerCase", "removePunctuationAndNumbers", "stopwording", "removeSingleChar", "removeDoubleChar"]
    newSentence = cleanSentence(sentence, sentenceProcList, tokenProcList)
    goldSentence = u"según hay riesgo generalizado tsunami tras sismo japón"
    self.assertEqual(newSentence, goldSentence)

  @unittest.skip("demonstrating skipping")
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
    text_field = 'status'
    new_text_field = 'status_clean'
    sentence_proc_list = {'removeUrl', 'removeUserMention'}
    token_proc_list = {'stemming', 'toLowerCase', 'removePunctuationAndNumbers',
      'stopwording', 'removeSingleChar', 'removeDoubleChar'}
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    proc = Processor(text_field, new_text_field, sentence_proc_list, token_proc_list)
    newRawObject = proc.processFile(rawObjects)
    self.assertEqual(rawObject, goldenRawObject)

  @unittest.skip("demonstrating skipping")
  def test_processFileUnicode(self):
    rawObject = {
      "date":u"Sun Aug 07 01:28:32 IST 2011",
      "id":u"100000335933878272",
      "user_id":u"71610408",
      "status":u"Según @NWS_PTWC, no hay riesgo generalizado de #tsunami tras el #sismo de Japón http://t.co/icErcNfSCf",
    }
    goldenRawObject = {
      "date":u"Sun Aug 07 01:28:32 IST 2011",
      "id":u"100000335933878272",
      "user_id":u"71610408",
      "status":u"Según @NWS_PTWC, no hay riesgo generalizado de #tsunami tras el #sismo de Japón http://t.co/icErcNfSCf",
      "status_clean":u"Según hay riesgo generalizado tsunami tras sismo Japón"
    }
    rawObjects = [rawObject]
    text_field = 'status'
    new_text_field = 'status_clean'
    sentence_proc_list = {'removeUrl', 'removeUserMention'}
    token_proc_list = {'stemming', 'toLowerCase', 'removePunctuationAndNumbers', 
      'stopwording', 'removeSingleChar', 'removeDoubleChar'}
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    proc = Processor(text_field, new_text_field, sentence_proc_list, token_proc_list)
    newRawObject = proc.processFile(rawObjects)
    self.assertEqual(rawObject, goldenRawObject)

  @unittest.skip("demonstrating skipping")
  def test_notValidProcessFile(self):
    rawObject = {
      "date":"Sun Aug 07 01:28:32 IST 2011",
      "id":"100000335933878272",
      "user_id":"71610408",
      "status":"@baloji you were so awesome, it was amazing and you were shining like the star that you are...MERCI!! #baloji i_i"
      }
    rawObjects = [rawObject]
    text_field = 'otherfield'
    new_text_field = 'status_clean'
    sentence_proc_list = {'removeUrl', 'removeUserMention'}
    token_proc_list = {'stemming', 'toLowerCase', 'removePunctuationAndNumbers', 
      'stopwording', 'removeSingleChar', 'removeDoubleChar'}
    functions.stopwords = load_stopwords('etc/stopwords_en.txt')
    proc = Processor(text_field, new_text_field, sentence_proc_list, token_proc_list)
    proc = Processor(config)
    self.assertRaises(Exception, proc.processFile, rawObjects)

  #@unittest.skip("avoid big files")
  def test_cleaner(self):
    rawParams = {
      'input_file':'etc/example.tsv',
      'output_file':'output.tmp',
      'config_file':'etc/example.conf',
    }
    params = objects.Configuration(param_fields, rawParams)
    config = generate_config(conf_fields, params.config_file)
    if isfile(params.output_file):
      remove(params.output_file)
    cleaner(params, config)
    self.assertTrue(isfile(params.output_file))
    self.assertEqual(wordCount(" to ", params.output_file), 0)
    self.assertEqual(wordCount(" photo ", params.output_file), 0)

