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

class TestCleanerFunctions(unittest.TestCase):
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
        goldenTokens = ["Hello", "did", "n't", "very", "happy", "1313"]
        tokens = tokenize(sentence)
        for i in range(0, len(tokens)):
            self.assertEqual(tokens[i], goldenTokens[i])

    def test_sentenize(self):
        tokens = ["Hello", "I", "'m", "very", "happy", "1313"]
        goldenSentence = "Hello I 'm very happy 1313"
        self.assertEqual(sentenize(tokens), goldenSentence)

    def test_sentenceCleaner(self):
        sentence = "Hello I'm very happy 1313"
        tokens = tokenize(sentence)
        newTokens = setenceCleaner(tokens, [stemming,
            removePunctuationAndNumbers, toLowerCase, stopwording])

    def test_stemming(self):
        sentence = ["boys", "women", "homes", "n't", "cars", "archives"]
        sentenceStemmed = ["boy", "woman", "home", "not", "car", "archive"]
        for i in range(0, len(sentence)):
            self.assertEqual(stemming(sentence[i]), sentenceStemmed[i])

    def test_toLowerCase(self):
        sentence = ["bOys", "WOMEN", "Homes", "MeN", "cARs", "aRchIvES"]
        sentenceLowerCase = ["boys", "women", "homes", "men", "cars", "archives"]
        for i in range(0, len(sentence)):
            self.assertEqual(toLowerCase(sentence[i]), sentenceLowerCase[i])

    def test_stopwording(self):
        sentence = ["At", "eight", "not", "on", "Thursday", "morning", 
            "Arthur", "didn't", "feel", "very", "good"]
        sentenceStopwording = ["At", "eight", "", "", "Thursday", "morning", 
            "Arthur", "didn't", "feel", "", "good"]
        for i in range(0, len(sentence)):
            self.assertEqual(stopwording(sentence[i]), sentenceStopwording[i])

    def test_removePunctuationAndNumbers(self):
        sentence = ['at', '8', "o'clock", 'on', '(', 'thursday', ')', 'morning',
            'Arthur', 'did', "nt", 'feel', 'very', 'good', '.']
        sentenceRemove = ['at', '', "oclock", 'on', '', 'thursday', '', 'morning',
            'Arthur', 'did', "nt", 'feel', 'very', 'good', '']
        for i in range(0, len(sentence)):
            self.assertEqual(removePunctuationAndNumbers(sentence[i]), sentenceRemove[i])

    def test_removeSingleChar(self):
        sentence = ['at', '8', "o'clock", 'on', '(', 'Thursday', ')', 'morning',
            'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
        sentenceRemove = ['at', '', "o'clock", 'on', '', 'Thursday', '', 'morning',
            'Arthur', 'did', "n't", 'feel', 'very', 'good', '']
        for i in range(0, len(sentence)):
            self.assertEqual(removeSingleChar(sentence[i]), sentenceRemove[i]) 
        
    def test_cleanSentence(self):
        sentence = ("At 8 o'clock on Thursday morning, the boys and " +
            "girls didn't feel very good.")
        newSentence = cleanSentence(sentence)
        goldSentence = "oclock thursday morning boy girl feel good"
        self.assertEqual(newSentence, goldSentence)

    def test_processLine(self):
        line = ("Sun Aug 07 01:28:32 IST 2011	100000335933878272	71610408" + 
            "	@baloji you were so awesome, it was amazing and you were" + 
            " shining like the star that you are...MERCI!! #baloji")
        goldenLine = ("Sun Aug 07 01:28:32 IST 2011	100000335933878272" + 
            "	71610408	awesome wa amazing shining like star" + 
            " merci baloji	")
        newLine = processLine(line)
        self.assertEqual(newLine, goldenLine)

    def test_processFile(self):
        path = "/home/pablo/data/run-adapter-fsd-db/Sun_Aug_07_01_00_00_IST_2011.tsv"
        with open(path, 'r') as contentFile:
            fullText = contentFile.read()
        processFile(fullText)

    def test_cleaner(self):
        path = "/home/pablo/data/run-adapter-fsd-db/Sun_Aug_07_01_00_00_IST_2011.tsv"
        cleaner(path, path + ".clean")
        self.assertTrue(isfile(path + ".clean"))

