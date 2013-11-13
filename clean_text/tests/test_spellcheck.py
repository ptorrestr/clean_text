import unittest

from clean_text.spellcheck import correct

class TestSpellChecker(unittest.TestCase):
    def test_correct(self):
        words = ["dont", "lol", "wan", "haha", "fuckin", "weird", "pic", "pls", "plz", "kno"]
        correctWords = ["dont", "ll", "wan", "hata", "fucking", "weird", "mic", "pus", "ply", "no"]
        for i in range(0, len(words)):
            self.assertEqual(correct(words[i]), correctWords[i])
