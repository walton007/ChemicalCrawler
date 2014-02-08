import urllib2
from lxml import html
from utilities.utilities import getEncoding
from utilities.logger import GetLogger
from utilities.timeUtility import SleepTimer
from model.chemiInfo import ChemiInfo

logger = GetLogger()

#db is pymongo.db
cnt = 0
def SpiderProductNAMEList(entryURL, cbChemiInfoHandler):
    visitedURLs = set()
    unvisitedURLs = []
    logger.info( 'entryURL:'+ entryURL)
    pos = entryURL.rfind('/')
    baseHref, entryUrlPath = entryURL[:pos], entryURL[pos:]
    unvisitedURLs.append(entryUrlPath)

    def visitURL(targetURL):
        logger.info('begin visit url: '+targetURL)
        global cnt
        cnt = cnt+1

        timer = SleepTimer(2)

        if cnt > 1200:
            logger.warn( 'Early Return')
            return

        content = urllib2.urlopen(targetURL).read()
        content = content.decode(getEncoding(content))
        doc = html.document_fromstring(content)

        if cnt == 1:
            #all product names from A->Z
            allAZ = doc.cssselect('#_ctl0_ContentPlaceHolder1_ProductClassLink a')
            for alink in allAZ:
                href = alink.get('href')
                unvisitedURLs.insert(0, href)
        if cnt == 2:
            #for debug usage
            return

        alltrs = doc.cssselect('table tr')
        if len(alltrs) == 0:
            return

        for tr in alltrs[1:]:
            tds = tr.cssselect('td')
            enNameElem, zhNameElem, casElem, mfElem = tds
            #get enName and enNameLink
            alink = enNameElem.cssselect('a')[0]
            enNameLink = alink.get('href')
            enName = alink.text

            #get zhName and zhNameLink
            zhName = zhNameElem.cssselect('span')[0].text

            #get CAS and CASLink
            cas = casElem.cssselect('span')[0].text

            #get mf
            mf = mfElem.cssselect('span')[0].text

            chemInfo = ChemiInfo(enName, zhName, enNameLink, None, cas, None, mf)
            if cbChemiInfoHandler:
                cbChemiInfoHandler.process(chemInfo)

        #other links need to be visited
        otherLinks = doc.cssselect('div[align="center"] a[onclick="blur()"]')
        logger.info( 'ele otherLinks: %d'%len(otherLinks))
        incLink = 0
        for ele in otherLinks:
            href = ele.get('href')
            if href in visitedURLs:
                continue
            else:
                unvisitedURLs.insert(0, href)
                incLink = incLink+1

        logger.info( 'end visit url, visit cnt: '+str(cnt))
        timer.conditionSleep()


    while len(unvisitedURLs) > 0:
        urlPath = unvisitedURLs.pop()
        if urlPath in visitedURLs:
            continue

        #visit this url and get html page
        targetURL = '/'.join([baseHref, urlPath])
        visitURL(targetURL)


if __name__ == '__main__':
    print 'SpiderProductNAMEList'
