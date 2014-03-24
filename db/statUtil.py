from mongodb import MongoDBFactory

class StatisticHelper(object):
    def   __init__(self, scheme):
        self.db = MongoDBFactory.GetDB('statisticDB')
        self.dbOne = MongoDBFactory.GetDB('chemicalDB')
        self.scheme = scheme
        self.allVisitedSet = set()
        '''
        print 'start load statistic data'
        for rec in self.db.find(scheme):
            if rec['visitStatus'] == 'visited':
                self.allVisitedSet.add(rec['urlpath'])
        print 'end load statistic data len rec:', len(self.allVisitedSet)
        '''


    def isUrlVisited(self, url):
        return url in self.allVisitedSet

        #rst = self.db.find(self.scheme, {"urlpath": url,  'visitStatus': 'visited'})
        #return rst.count() > 0

    def markUrlVisited(self, url):
        self.db.insert(self.scheme, {'urlpath': url, 'visitStatus': 'visited'})
        self.allVisitedSet.add(url)

    def markUrlBadVisited(self, url):
        self.db.insert(self.scheme, {'urlpath': url, 'visitStatus': 'badvisited'})
        self.allVisitedSet.add(url)

    def isCASVisited(self, cas):
        rst = self.dbOne.find('OneDB', {"CAS": cas})
        return rst.count() > 0

    def reset(self):
        pass

def test():
    p = StatisticHelper('statisOne')
    print p.isUrlVisited('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB41260892.htm')
    print p.isUrlVisited('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB41260s892.htm')
    p.markUrlVisited('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB41260s892.htm')
    print p.isUrlVisited('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB41260s892.htm')


if __name__ == '__main__':
    test()
