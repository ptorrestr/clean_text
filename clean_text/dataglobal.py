"""
====
dataglobal
====
"""

def init():
  """
  Initialise an list with global scope. It is used only to get the stopwordsPath.
  """
  global list
  list = { 
   "stopwordsPath":"",
   "stopwordsAlreadyUploaded":False,
  }
