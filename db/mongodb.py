from pymongo import MongoClient

from myConfig import GetGlobalConfig
globalConfig = GetGlobalConfig()
dbhost = globalConfig['dbhost']
dbport = globalConfig['dbport']
dbuser = globalConfig['dbuser']
dbpassword = globalConfig['dbpassword']
dbanonymous = globalConfig['dbanonymous']
print 'dbhost:', dbhost
print 'dbport:', dbport

if dbanonymous:
    dburi = "mongodb://%s:%s"%(dbhost, dbport)
else:
    dburi = "mongodb://%s:%s@%s:%s"%(dbuser, dbpassword, dbhost, dbport)

print dburi

from utilities.logger import GetLogger
logger = GetLogger()

#object should be some interface like insert interface
class DBWrapper(object):
    totalRec = 0
    def __init__(self, db):
        self.db = db

    def insert(self, schema, obj):
        collection = self.db[schema]
        if isinstance(obj, dict):
            print 'schema: ', schema
            DBWrapper.totalRec = DBWrapper.totalRec +1
            logger.info('insert: %s totalRec:%s '%(len(obj), DBWrapper.totalRec))
            collection.insert(obj)
        else:
            collection.insert(obj.__dict__)

    def find(self, schema, conditonObj):
        collection = self.db[schema]
        return collection.find(conditonObj)

    def ClearScheme(self, schema):
        #return
        collection = self.db[schema]
        collection.drop()

class MongoDBFactory(object):
    connection=MongoClient(dburi)
    @classmethod
    def GetDB(cls, dbName):
        return DBWrapper(cls.connection[dbName])

if __name__ == '__main__':
    MongoDBFactory.GetDB('chemicalDB')
