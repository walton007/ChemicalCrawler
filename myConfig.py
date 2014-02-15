import ConfigParser
import os
import sys
from datetime import datetime

filePath = "chem.conf"
len(sys.argv)
for i in xrange(0, len(sys.argv)):
    if sys.argv[i] == '-conf':
        filePath = sys.argv[i+1]
        break

modifiedTime = None

globalConfig = {
    'dbhost': 'localhost',
    'dbport': '27017',
    'dbclear': False,
    'dbschema':'',
    'dbuser': 'walton',
    'dbpassword': 'walton',
    'dbanonymous': True,

    'duration' : 3,
    'waitDuration': 20,

    'crawlAllPage' : False,
    'entryURL': 'http://www.chemicalbook.com/ShowAllProductByIndexID_CAS_16_0.htm',
    'httpProxy':'',

    'filename': 'test.log',

    'debugOpen': False,
    'debugOnePage': False
}

def UpdateConfig(updateAll):
    print 'UpdateConfig'
    try:
        global filePath, modifiedTime, globalConfig
        modifiedTime = os.path.getmtime(filePath)
        cf = ConfigParser.ConfigParser()
        cf.read(filePath)
        globalConfig['duration'] = cf.getfloat("strategy", "duration")
        globalConfig['waitDuration'] = cf.getfloat("strategy", "waitDuration")

        if updateAll:
            globalConfig['dbhost'] = cf.get("db", "host")
            globalConfig['dbport'] = cf.getint("db", "port")
            globalConfig['dbclear'] = cf.getboolean("db", "clear")
            globalConfig['dbschema'] = cf.get("db", "schema")
            globalConfig['dbuser'] = cf.get("db", "user")
            globalConfig['dbpassword'] = cf.get("db", "password")
            globalConfig['dbanonymous'] = cf.getboolean("db", "anonymous")

            globalConfig['crawlAllPage'] = cf.getboolean("crawl", "crawlAllPage")
            globalConfig['entryURL'] = cf.get("crawl", "entryURL")
            globalConfig['httpProxy'] = cf.get("crawl", "httpProxy")

            globalConfig['filename'] = cf.get("log", "filename")

            globalConfig['debugOpen']=cf.getboolean("debug", "open")
            globalConfig['debugOnePage']=cf.getboolean("debug", "onepage")

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

def GetWaitDuration():
    waitDuration = GetGlobalConfig()['waitDuration']
    return waitDuration
