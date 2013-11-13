import globals

def setStopwordsPath(stopwordsPath):
  globals.list["stopwordsPath"] = stopwordsPath

def stopwords():
  stopwordsPath = globals.list["stopwordsPath"]
  stopwordsAlreadyUploaded = globals.list["stopwordsAlreadyUploaded"]

  # Is chacheStopword empty?
  if not stopwordsAlreadyUploaded:
    # Has the user set a path for stopwords?
    if not stopwordsPath == '':
      # load stopwords
      globals.list["stopwords"] = readListFile(stopwordsPath)
    else:
      globals.list["stopwords"] = []
    globals.list["stopwordsAlreadyUploaded"] = True
  return globals.list["stopwords"]

def readListFile(path):
  lines = []
  with open(path, "r") as listFile:
    for line in listFile:
      if not line.startswith("#") and len(line.strip()) > 0:
        lines.append(line.strip())
  return lines
