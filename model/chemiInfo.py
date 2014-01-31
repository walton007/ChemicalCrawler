class ChemiInfo(object):
    cnt = 0
    def __init__(self, enName, zhName, enNameLink, zhNameLink, cas, casLink, mf):
        self.enName = enName
        self.zhName = zhName
        self.enNameLink = enNameLink
        self.zhNameLink = zhNameLink
        self.cas = cas
        self.casLink = casLink
        self.mf = mf

    def descriptionF(self, fd):
        if self.zhName and ChemiInfo.cnt < 1:
            ChemiInfo.cnt = ChemiInfo.cnt+1
            #fd.write(self.zhName.encode('utf8'))
            fd.write(self.zhName.encode('utf8'))
            #print self.zhName
            print self.cas
            print self.cas


    def description(self):
        ChemiInfo.cnt = ChemiInfo.cnt+1
        if ChemiInfo.cnt ==21:
            print 99
        print 'ChemiInfo.cnt:',ChemiInfo.cnt
        print '\n'
        print 'enName: %s\n zhName:%s\n enNameLink:%s\n zhNameLink:%s\n cas:%s\n casLink:%s\n mf:%s\n'%( \
                                self.enName, self.zhName, self.enNameLink, self.zhNameLink, self.cas, self.casLink, self.mf)
