import logging

logger = logging.getLogger('clean_text')

languages = None

def get_languages():
  global languages
  if not languages:
    english = Language('english','etc/english_training_data.txt')
    languages = [ english ]
  return languages

def recognize_language(sentence, languages, threshold):
  if not languages:
    logger.warning('You need to train a model before use language recognition. Do nothing')
    return None
  lang = NGram(sentence, n = 3).find_match(languages, threshold = threshold)
  return lang

class Language(object):
  def __init__(self, name, file):
    self.name = name
    self.file = file
    self._standard_training()

  def _standard_training(self):
    logger.info('Training language detector for: ' + self.name)
    with open(self.file) as f:
      training_text = f.read()
    self.ngram = NGram(training_text)

# Developed by http://blog.ebookglue.com/?p=69 
# http://blog.ebookglue.com/write-language-detector-50-lines-python/
class NGram(object):
  def __init__(self, text, n = 3):
    self.length = None
    self.n = n
    self.table = {}
    self.parse_text(text)
    self.calculate_length()
 
  def parse_text(self, text):
    chars = ' ' * self.n # initial sequence of spaces with length n
    for letter in (" ".join(text.split()) + " "):
      chars = chars[1:] + letter # append letter to sequence of length n
      self.table[chars] = self.table.get(chars, 0) + 1 # increment count
 
  def calculate_length(self):
    """ Treat the N-Gram table as a vector and return its scalar magnitude
      to be used for performing a vector-based search.
    """
    self.length = sum([x * x for x in self.table.values()]) ** 0.5
    return self.length
 
  def __sub__(self, other):
    """ Find the difference between two NGram objects by finding the cosine
        of the angle between the two vector representations of the table of
        N-Grams. Return a float value between 0 and 1 where 0 indicates that
        the two NGrams are exactly the same.
    """
    # allows comparison with Language class directly
    if isinstance(other, Language):
      other = other.ngram
    if not isinstance(other, NGram):
      raise TypeError("Can't compare NGram with non-NGram object.")
    if self.n != other.n:
      raise TypeError("Can't compare NGram objects of different size.")
    total = 0
    for k in self.table:
      total += self.table[k] * other.table.get(k, 0)
    return 1.0 - (float(total) / (float(self.length) * float(other.length)))
 
  def find_match(self, languages, threshold = 0.7):
    """ Out of a list of NGrams that represent individual languages, return
        the best match.
    """
    candidate = min(languages, key = lambda n: self - n)
    if candidate.ngram - self > threshold:
      return None
    return candidate
