# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

from db import mongodb
from utilities.logger import GetLogger, SetLoggerFileName

logger = GetLogger()
#global configure
dbName = 'chemicalDB'

def DoSpiderProductCASList():
    logger.info('DoSpiderProductCASList')
    from spiderSites.ProductCASList import SpiderProductCASList
    from spiderSites.spiderSites import HandleProductCASListStrategy

    clear = True if '--CLEAR' in sys.argv else False
    db = mongodb.MongoDBFactory.GetDB(dbName)
    entryURL= 'http://www.chemicalbook.com/ProductCASList_12_0.htm'
    SpiderProductCASList(entryURL, HandleProductCASListStrategy(db, clear))


def DoSpiderProductNameList():
    logger.info('DoSpiderProductNameList')
    from spiderSites.ProductNAMEList import SpiderProductNAMEList
    from spiderSites.ProductNAMEListStrategy import HandleProductNAMEListStrategy
    clear = True if '--CLEAR' in sys.argv else False
    db = mongodb.MongoDBFactory.GetDB(dbName)
    entryURL= 'http://www.chemicalbook.com/ProductNameList_1_0.htm'
    SpiderProductNAMEList(entryURL, HandleProductNAMEListStrategy(db, clear))

def DoSpiderCASDetailList():
    print 1
    logger.info('DoSpiderCASDetailList')
    from spiderSites.ProductCASDetailList import SpiderCASDetailList
    from spiderSites.ProductCASDetailListStrategy import HandleCASDetailStrategy
    clear = True if '--CLEAR' in sys.argv else False
    db = mongodb.MongoDBFactory.GetDB(dbName)
    entryURL= 'http://www.chemicalbook.com/CASDetailList_0.htm'
    SpiderCASDetailList(entryURL, HandleCASDetailStrategy(db, clear))
    print 3

def DoSpiderCASIDList():
    logger.info('DoSpiderCASIDList')
    from spiderSites.CASIDList import SpiderCASIDList
    from spiderSites.CASIDListStrategy import HandleCASIDListStrategy
    from myConfig import GetGlobalConfig
    globalConfig = GetGlobalConfig()
    entryURL= globalConfig['entryURL']
    dbclear = globalConfig['dbclear']
    dbschema = globalConfig['dbschema']
    crawlAllPage = globalConfig['crawlAllPage']

    db = mongodb.MongoDBFactory.GetDB(dbName)
    SpiderCASIDList(entryURL, crawlAllPage, HandleCASIDListStrategy(db, dbclear, dbschema))

from myConfig import GetGlobalConfig
globalConfig = GetGlobalConfig()
print globalConfig
while False:
    pass

if '--CASLIST' in sys.argv:
    SetLoggerFileName('caslist')
    DoSpiderProductCASList()
if '--ProductNameLIST' in sys.argv:
    SetLoggerFileName('namelist')
    DoSpiderProductNameList()
if '--DetailCASLIST' in sys.argv:
    SetLoggerFileName('detailCASList')
    DoSpiderCASDetailList()
if True or '--CASIDLIST' in sys.argv:
    filename = globalConfig['filename']
    SetLoggerFileName(filename)
    DoSpiderCASIDList()
