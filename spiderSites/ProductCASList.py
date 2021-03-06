import urllib2
from lxml import html
from utilities.utilities import getEncoding
from utilities.logger import GetLogger
from utilities.timeUtility import SleepTimer
from model import ChemiInfo

logger = GetLogger()

#db is pymongo.db
cnt = 0
def SpiderProductCASList(entryURL, cbChemiInfoHandler):
    print 33
    visitedURLs = set()
    unvisitedURLs = []
    logger.info( 'entryURL:'+ entryURL)
    pos = entryURL.rfind('/')
    baseHref, entryUrlPath = entryURL[:pos], entryURL[pos:]
    unvisitedURLs.append(entryUrlPath)

    def visitURL(targetURL):
        logger.info('begin visit url: '+targetURL)
        print 'target:', targetURL

        global cnt
        cnt = cnt+1

        timer = SleepTimer(2)

        if cnt > 999999:
            logger.warn( 'Early Return')
            return

        content = urllib2.urlopen(targetURL).read()
        content = content.decode(getEncoding(content))
        doc = html.document_fromstring(content)

        print doc

        if cnt == 1:
            #all CAS names from 1->9
            all1to9 = doc.cssselect('#_ctl0_ContentPlaceHolder1_ProductClassLink a')
            for alink in all1to9:
                href = alink.get('href')
                unvisitedURLs.insert(0, href)

        alltrs = doc.cssselect('table tr')
        for tr in alltrs[1:]:
            tds = tr.cssselect('td')
            enNameElem, zhNameElem, casElem, mfElem = tds
            #get enName and enNameLink
            alink = enNameElem.cssselect('a')[0]
            enNameLink = alink.get('href')
            enName = alink.text

            #get zhName and zhNameLink
            alink = zhNameElem.cssselect('a')[0]
            zhNameLink = alink.get('href')
            zhName = alink.text

            #get CAS and CASLink
            alink = casElem.cssselect('a')[0]
            casLink = alink.get('href')
            cas = alink.text

            #get mf
            mf = mfElem.cssselect('span')[0].text

            chemInfo = ChemiInfo(enName, zhName, enNameLink, zhNameLink, cas, casLink, mf)
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
                unvisitedURLs.append(href)
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
    targetURL = r'''http://www.chemicalbook.com/ProductCASList_12_0.htm'''
    content = urllib2.urlopen(targetURL).read()
    content = content.decode('UTF-8')
    doc = html.document_fromstring(content)
    otherLinks = doc.cssselect('a[onclick="blur()"]')
    for ele in otherLinks:
        href = ele.get('href')
        print href
