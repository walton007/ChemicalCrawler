from mongodb import MongoDBFactory

class StatisticHelper(object):
    def   __init__(self, scheme):
        self.db = MongoDBFactory.GetDB('statisticDB')
        self.scheme = scheme

    def isUrlVisited(self, url):
        rst = self.db.find(self.scheme, {"urlpath": url,  'visitStatus': 'visited'})
        return rst.count() > 0

    def markUrlVisited(self, url):
        self.db.insert(self.scheme, {'urlpath': url, 'visitStatus': 'visited'})

    def reset(self):
        pass
