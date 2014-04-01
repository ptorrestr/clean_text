from clean_text import dataglobal

def setStopwordsPath(stopwordsPath):
  dataglobal.list["stopwordsPath"] = stopwordsPath

def stopwords():
  stopwordsPath = dataglobal.list["stopwordsPath"]
  stopwordsAlreadyUploaded = dataglobal.list["stopwordsAlreadyUploaded"]

  # Is chacheStopword empty?
  if not stopwordsAlreadyUploaded:
    # Has the user set a path for stopwords?
    if not stopwordsPath == '':
      # load stopwords
      dataglobal.list["stopwords"] = readListFile(stopwordsPath)
    else:
      dataglobal.list["stopwords"] = []
    dataglobal.list["stopwordsAlreadyUploaded"] = True
  return dataglobal.list["stopwords"]

def readListFile(path):
  lines = []
  try:
    with open(path, "r") as listFile:
      for line in listFile:
        if not line.startswith("#") and len(line.strip()) > 0:
          lines.append(line.strip())
  except IOError:
    raise
  return lines

confFields = [
  {"name":"overWriteOutputFile", "kind":"mandatory", "type":bool},
  {"name":"bufferSize", "kind":"mandatory", "type":int},
  {"name":"splitCriteriaLine", "kind":"mandatory", "type":str},
  {"name":"stopwordFile", "kind":"mandatory", "type":str},
  {"name":"sentenceProcList", "kind":"mandatory", "type":list},
  {"name":"tokenProcList", "kind":"mandatory", "type":list},
  {"name":"fields", "kind":"mandatory", "type":list},
  {"name":"textField", "kind":"mandatory", "type":str},
  {"name":"newFields", "kind":"mandatory", "type":list},
  {"name":"newTextField", "kind":"mandatory", "type":str},
  ]

confDefault = {
  "overWriteOutputFile":True,
  "bufferSize":200,
  "splitCriteriaLine":"\t",
  "stopwordFile":"",
  "sentenceProcList":"removeUrl removeUserMention",
  "tokenProcList":"stemming toLowerCase removePunctuationAndNumbers stopwording removeSingleChar removeDoubleChar",
  "fields":"date id hash user_id status",
  "textField":"status",
  "newFields":"date id hash user_id status status_clean",
  "newTextField":"status_clean",
  }
