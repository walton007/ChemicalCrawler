import pymongo
from myConfig import GetGlobalConfig
globalConfig = GetGlobalConfig()
dbhost = globalConfig['dbhost']
dbport = globalConfig['dbport']
print 'dbhost:', dbhost
print 'dbport:', dbport

#object should be some interface like insert interface
class DBWrapper(object):
    def __init__(self, db):
        self.db = db

    def insert(self, schema, obj):
        collection = self.db[schema]
        if isinstance(obj, dict):
            print 'insert: ', len(obj)
            print 'schema: ', schema
            collection.insert(obj)
        else:
            collection.insert(obj.__dict__)

    def ClearScheme(self, schema):
        #return
        collection = self.db[schema]
        collection.drop()

class MongoDBFactory(object):
    connection=pymongo.Connection(dbhost, dbport)
    @classmethod
    def GetDB(cls, dbName):
        return DBWrapper(cls.connection[dbName])

if __name__ == '__main__':
    MongoDBFactory.GetDB('chemicalDB')
