from StrategyInterface import HandleChemiInfoInterface
#db is pymongo.db
class HandleCASIDListStrategy(HandleChemiInfoInterface):
    #db should support some interface like insert
    SCHEMA = 'CASIDList'
    def __init__(self, db, clearSchema):
        self.db = db
        if clearSchema:
            db.ClearScheme(self.SCHEMA)

    def process(self, chemInfo):
        self.db.insert(self.SCHEMA,chemInfo)
