import ConfigParser
import os
from datetime import datetime

filePath = "chem.conf"
modifiedTime = None

globalConfig = {
    'dbhost': 'localhost',
    'dbport': '27017',
    'dbclear': False,
    'dbschema':'',

    'duration' : 3,

    'crawlAllPage' : False,
    'entryURL': 'http://www.chemicalbook.com/ShowAllProductByIndexID_CAS_16_0.htm',
    'httpProxy':'',

    'filename': 'test.log'
}

def UpdateConfig(updateAll):
    print 'UpdateConfig'
    try:
        global filePath, modifiedTime, globalConfig
        modifiedTime = os.path.getmtime(filePath)
        cf = ConfigParser.ConfigParser()
        cf.read(filePath)
        globalConfig['duration'] = cf.getfloat("strategy", "duration")


        if updateAll:
            globalConfig['dbhost'] = cf.get("db", "host")
            globalConfig['dbport'] = cf.getint("db", "port")
            globalConfig['dbclear'] = cf.getboolean("db", "clear")
            globalConfig['dbschema'] = cf.get("db", "schema")

            globalConfig['crawlAllPage'] = cf.getboolean("crawl", "crawlAllPage")
            globalConfig['entryURL'] = cf.get("crawl", "entryURL")
            globalConfig['httpProxy'] = cf.get("crawl", "httpProxy")

            globalConfig['filename'] = cf.get("log", "filename")

        print globalConfig
    except Exception as err:
        print err

def GetGlobalConfig():
    global filePath, modifiedTime, globalConfig
    if modifiedTime is None:
        UpdateConfig(True)
    else:
        curModifiedTime = os.path.getmtime(filePath)
        if curModifiedTime > modifiedTime:
            UpdateConfig(False)

    return globalConfig


def GetSleepDuration():
    sleepDuration = GetGlobalConfig()['duration']
    return sleepDuration
