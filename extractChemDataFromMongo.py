import os
from utilities.logger import GetLogger, SetLoggerFileName
logger = GetLogger()

'''
conn = psycopg2.connect(host ="115.28.62.4", port="5432", database="mydb", user="postgres", password="postgres")

print conn

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

try:
    cur.execute("SELECT * FROM barf")
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",  (100, "abc'def"))
except Exception, e:
    print e
'''

class MolDataExtracter(object):
    moltable = 'MolTable'

    def __init__(self):
        self.initMongoClient()
        self.initPostgreClient()
        self.loadRecords()

    def initPostgreClient(self):
        import psycopg2
        import psycopg2.extras
        self.connPostgres = psycopg2.connect(host = "115.28.62.4", port="5432", database="mydb", user="postgres", password="postgres")
        self.curPostgresDict = self.connPostgres.cursor(cursor_factory=psycopg2.extras.DictCursor)



    def initMongoClient(self):
        from pymongo import MongoClient

        self.connMongo = MongoClient("mongodb://%s:%s@%s:%s"%('walton', 'walton', "115.28.62.4", '27017'))
        self.connMongoDB = self.connMongo['chemicalDB']
        self.connMongoCollection = self.connMongoDB['OneDB']
        #self.connMongoCollection = self.connMongoDB['allpages']

    def commitPostgre(self):
        self.connPostgres.commit()

    def loadRecords(self):
        self.records = set()
        sql = '''SELECT * FROM bingo.record;'''
        cursor = self.curPostgresDict
        cursor.execute(sql)
        self.commitPostgre()

        for rec in cursor:
            self.records.add(rec[0])



    def extract(self, num):
        cnt = 0
        totalcnt = 0
        if num > 1:
            alldata = self.connMongoCollection.find().sort("_id").limit(num)
            # self.connMongoCollection.find({'zhName': {"$exists" : True, "$ne" : None} }).sort("_id").limit(num)
        else:
            alldata = self.connMongoCollection.find().sort("_id")
        for data in alldata:
             recordid = str(data['_id'])
             if recordid in self.records:
                logger.info("ignore %s", recordid)
                continue

             cnt = (cnt + 1) %100
             totalcnt=totalcnt+1
             if cnt == 0:
                logger.info('extract %s record', totalcnt)
                self.commitPostgre()

             self.insertDataToPostgre(self.curPostgresDict, data)


        #commit again
        self.commitPostgre()
        logger.info('[finish] extract %s record', totalcnt)
        logger.info('Return')

    def insertDataToPostgre(self, cursor, data):
        sql = '''INSERT INTO bingo."%s"(
            cas, cbnumber, properties, zhname, enname, zhsynonym, ensynonym,
            molecular, formula, mofile)
            VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s,
            %%s, %%s) RETURNING id; '''%(self.moltable)
        param = (data['CAS'], data['CBNumber'], str(data['chemicalProperties']),
            data['zhName'],
            data['enName'], data['zhSynonym'],  data['enSynonym'],  data['molecular'],
            data['formula'],  data['mofile'])

        cursor.execute(sql, param)

        sqlRecord = '''INSERT INTO bingo.record(id) VALUES (%s);'''
        paramRecord = (str(data['_id']),)
        cursor.execute(sqlRecord, paramRecord)
        #update set in memory
        self.records.add(paramRecord[0])

    def testInsertDataToPostgre(self):
        sql = '''INSERT INTO bingo."ChemTable"(
            cas, cbnumber, properties, zhname, enname, zhsynonym, ensynonym,
            molecular, formula, mofile)
            VALUES ('a', 'b', 'c', '{}', 'e', 'f', 'g', 'h',
            'i', 'j') RETURNING id; '''

        sql = '''INSERT INTO bingo."ChemTable"(
            cas, cbnumber, properties, zhname, enname, zhsynonym, ensynonym,
            molecular, formula, mofile)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s) RETURNING id; '''

        self.curPostgresDict.execute(sql, ('a', 'b', 'c', '{}', '[e]|', 'f', 'g', 'h',
            'i', 'j') )
        self.connPostgres.commit()

    def testCheckData(self):
        sql = ''' select bingo.CheckMolecule(mofile) , bingo."ChemTable".* from bingo."ChemTable" where bingo.CheckMolecule(mofile) is not null;
        '''

        file = open('postgretest.log',  'wb')
        self.curPostgresDict.execute(sql)
        cur = self.connPostgres.cursor('checkcursor')
        cur = self.curPostgresDict
        cur.execute(sql)
        for record in cur.fetchmany(2):
            print record
            #file.write(record)
        file.close()



#MolDataExtracter()
MolDataExtracter().extract(0)
#MolDataExtracter().testCheckData()



'''
SELECT
  "ChemTable".zhsynonym,
  "ChemTable".id,
  "ChemTable".cbnumber,
  "ChemTable".cas,
  "ChemTable".properties,
  "ChemTable".zhname,
  "ChemTable".enname,
  "ChemTable".ensynonym
FROM
  bingo."ChemTable"
WHERE
  "ChemTable".ensynonym ILIKE '_%dihy_%';
  '''
'''
delete  from bingo."MolTable";
delete  from bingo."record";
'''
