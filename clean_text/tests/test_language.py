import unittest

from clean_text.language import recognize_language
from clean_text.language import Language

class test_language(unittest.TestCase):
  def setUp(self):
    pass

  def test_standard_training(self):
    english = Language('english', 'etc/english_training_data.txt')

  def test_recognize_language(self):
    english = Language('english', 'etc/english_training_data.txt')
    languages = [ english ]
    lang = recognize_language('this is a simple sentence', languages, 0.85)
    self.assertEqual(lang.name, english.name)
