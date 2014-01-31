# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

from db import mongodb

#global configure
dbName = 'chemicalDB'

def DoSpiderProductCASList():
    from spiderSites import SpiderProductCASList, HandleProductCASListStrategy
    clear = True if '--CLEAR' in sys.argv else False
    db = mongodb.MongoDBFactory.GetDB(dbName)
    entryURL= 'http://www.chemicalbook.com/ProductCASList_12_0.htm'
    SpiderProductCASList(entryURL, HandleProductCASListStrategy(db, clear))

def SpiderProductNameList():
    pass

def SpiderCASDetailList():
    pass

if __name__ == '__main__':
    if '--CASLIST' in sys.argv:
        DoSpiderProductCASList()
