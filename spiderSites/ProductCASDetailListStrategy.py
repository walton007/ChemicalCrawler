from StrategyInterface import HandleChemiInfoInterface
#db is pymongo.db
class HandleCASDetailStrategy(HandleChemiInfoInterface):
    #db should support some interface like insert
    SCHEMA = 'CASDetailList'
    def __init__(self, db, clearSchema):
        self.db = db
        if clearSchema:
            db.ClearScheme(self.SCHEMA)

    def process(self, chemInfo):
        self.db.insert(self.SCHEMA,chemInfo)
