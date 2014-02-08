import pymongo

#object should be some interface like insert interface
class DBWrapper(object):
    def __init__(self, db):
        self.db = db

    def insert(self, schema, obj):
        #return
        collection = self.db[schema]
        if isinstance(obj, dict):
            collection.insert(obj)
        else:
            collection.insert(obj.__dict__)

    def ClearScheme(self, schema):
        #return
        collection = self.db[schema]
        collection.drop()

class MongoDBFactory(object):
    connection=pymongo.Connection('localhost',27017)
    @classmethod
    def GetDB(cls, dbName):
        return DBWrapper(cls.connection[dbName])

if __name__ == '__main__':
    MongoDBFactory.GetDB('chemicalDB')
