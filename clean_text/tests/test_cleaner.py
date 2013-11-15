import unittest

from os.path import isfile

from clean_text.cleaner import removeUrl
from clean_text.cleaner import removeUserMention
from clean_text.cleaner import setenceCleaner
from clean_text.cleaner import tokenize
from clean_text.cleaner import sentenize
from clean_text.cleaner import stemming
from clean_text.cleaner import stopwording
from clean_text.cleaner import removePunctuationAndNumbers
from clean_text.cleaner import toLowerCase
from clean_text.cleaner import removeSingleChar
from clean_text.cleaner import cleanSentence
from clean_text.cleaner import processLine
from clean_text.cleaner import processFile
from clean_text.cleaner import cleaner
from clean_text.data import setStopwordsPath
from clean_text.globals import init

class TestCleanerFunctions(unittest.TestCase):
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

    def test_sentenceCleaner(self):
        sentence = "Hello I'm very happy 1313"
        tokens = tokenize(sentence)
        newTokens = setenceCleaner(tokens, [stemming,
            removePunctuationAndNumbers, toLowerCase, stopwording])

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
        
    def test_cleanSentence(self):
        sentence = ("At 8 o'clock on Thursday morning, the boys and " +
            "girls didn't feel very good.")
        newSentence = cleanSentence(sentence)
        goldSentence = "oclock thursday morning boy girl feel good"
        self.assertEqual(newSentence, goldSentence)

    def test_processLine(self):
        line = ("Sun Aug 07 01:28:32 IST 2011	100000335933878272	71610408" + 
            "	@baloji you were so awesome, it was amazing and you were" + 
            " shining like the star that you are...MERCI!! #baloji i_i")
        goldenLine = ("Sun Aug 07 01:28:32 IST 2011	100000335933878272" + 
            "	71610408	awesome amaze shin like star" + 
            " merci baloji	")
        newLine = processLine(line)
        self.assertEqual(newLine, goldenLine)

    def test_processFile(self):
        path = "./etc/example.tsv"
        with open(path, 'r') as contentFile:
            fullText = contentFile.read()
        processFile(fullText)

    def test_cleaner(self):
        path = "./etc/example.tsv"
        stopwordsPath = "./etc/stopwords_en.txt"
        cleaner(path, path + ".clean", stopwordsPath)
        self.assertTrue(isfile(path + ".clean"))


