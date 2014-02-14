def init():
  global list
  list = { 
   "stopwordsPath":"",
   "stopwordsAlreadyUploaded":False,
  }

confFields = [
  {"name":"splitCriteriaFile", "kind":"mandatory", "type":str},
  {"name":"splitCriteriaLine", "kind":"mandatory", "type":str},
  {"name":"textColumnPosition", "kind":"mandatory", "type":int},
  {"name":"newTextColumnPosition", "kind":"mandatory", "type":int},
  {"name":"stopwordFile", "kind":"mandatory", "type":str},
  {"name":"sentenceProcList", "kind":"mandatory", "type":list},
  {"name":"tokenProcList", "kind":"mandatory", "type":list},
  ]

confDefault = {
  "splitCriteriaFile":"\n",
  "splitCriteriaLine":"\t",
  "textColumnPosition":2,
  "newTextColumnPosition":3,
  "stopwordFile":"",
  "sentenceProcList":"removeUrl, removeUserMention",
  "tokenProcList":"stemming, toLowerCase, removePunctuationAndNumbers, stopwording, removeSingleChar, removeDoubleChar"
  }
