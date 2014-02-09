from StrategyInterface import HandleChemiInfoInterface
#db is pymongo.db
class HandleCASIDListStrategy(HandleChemiInfoInterface):
    #db should support some interface like insert
    SCHEMA = 'CASIDCollection'
    def __init__(self, db, clearSchema, schemaName):
        self.db = db
        if schemaName is not None:
            self.SCHEMA = schemaName

        if clearSchema:
            db.ClearScheme(self.SCHEMA)

    def process(self, chemInfo):
        self.db.insert(self.SCHEMA,chemInfo)
