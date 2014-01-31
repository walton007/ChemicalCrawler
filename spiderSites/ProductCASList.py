import urllib2
from lxml import html

if __name__ != '__main__':
    from utilities import getEncoding
    from utilities import SleepTimer
    from model import ChemiInfo


#db is pymongo.db
cnt = 0
def SpiderProductCASList(entryURL, cbChemiInfoHandler):
    visitedURLs = set()
    unvisitedURLs = []
    print 'entryURL:', entryURL
    pos = entryURL.rfind('/')
    baseHref, entryUrlPath = entryURL[:pos], entryURL[pos:]
    unvisitedURLs.append(entryUrlPath)

    def visitURL(targetURL):
        print 'begin visit url: '+targetURL
        global cnt
        cnt = cnt+1

        timer = SleepTimer()

        if cnt > 999999:
            print 'Early Return'
            return

        content = urllib2.urlopen(targetURL).read()
        content = content.decode(getEncoding(content))
        doc = html.document_fromstring(content)

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
        otherLinks = doc.cssselect('a[onclick="blur()"]')
        for ele in otherLinks:
            href = ele.get('href')
            if href in visitedURLs:
                continue
            else:
                unvisitedURLs.append(href)

        print 'end visit url, visit cnt: '+str(cnt)
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
