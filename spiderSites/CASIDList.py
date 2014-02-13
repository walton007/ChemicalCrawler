from myConfig import GetSleepDuration, GetGlobalConfig
globalConfig = GetGlobalConfig()

import urllib2
import socket

socket.setdefaulttimeout(20)

if len(globalConfig['httpProxy']) > 7:
    proxy = globalConfig['httpProxy'] #'http://127.0.0.1:8087'
    proxy_support = urllib2.ProxyHandler({'http': proxy})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


from lxml import html

from utilities.utilities import getEncoding
from utilities.logger import GetLogger
from utilities.timeUtility import SleepTimer

logger = GetLogger()
baseHref = 'http://www.chemicalbook.com'
errVisitPages = []

def GetCASDetail(casURL):
    logger.info('  begin get CASDetail:'+casURL)
    timer = SleepTimer(GetSleepDuration())
    request = urllib2.urlopen(casURL)
    content = request.read()
    request.close()
    content = content.decode(getEncoding(content))
    doc = html.document_fromstring(content)

    #parse ProductIntroduction
    ProductIntroduction = doc.cssselect('#ProductIntroduction table[border="0"]')[0]
    trs = ProductIntroduction.cssselect('tr')
    CAS = trs[0].getprevious().cssselect('b')[0].text
    enName = trs[0].cssselect('td b')[0].text
    enSynonym = trs[1].cssselect('td')[1].text
    zhName = trs[2].cssselect('td b')[0].text
    zhSynonym = trs[3].cssselect('td')[1].text
    CBNumber = trs[4].cssselect('td')[1].text
    molecular = trs[6].cssselect('td')[1].text
    formula = trs[7].cssselect('td')[1].text
    mofilelink = trs[8].cssselect('td a')[0].get('href')

    request = urllib2.urlopen('/'.join([baseHref, mofilelink]))
    mofile = request.read()
    request.close()
    mofile = mofile.decode(getEncoding(mofile))

    chemicalPropertiesObj = {}
    ChemicalPropertiesArray = doc.cssselect('#ChemicalProperties')
    if len(ChemicalPropertiesArray) > 0:
        ChemicalProperties = ChemicalPropertiesArray[0]
        propertiesNameArray = ChemicalProperties.cssselect('table tr td.detailLtd span')
        propertiesValueArray = ChemicalProperties.cssselect('table tr td.detailRtd span')
        if len(propertiesNameArray) != len(propertiesValueArray):
            logger.error(casURL+' ChemicalPropertiesArray not equal')
        else:
            for i in xrange(0, len(propertiesNameArray)):
                valElement = propertiesValueArray[i]
                if len(valElement.cssselect('a')) > 0:
                    continue
                nameElement = propertiesNameArray[i]
                chemicalPropertiesObj[nameElement.text] = valElement.text
    else:
        pass

    logger.info('  end get CASDetail:'+casURL)
    timer.conditionSleep();

    return {    'CAS' : CAS,
    'enName' :enName,
    'enSynonym' :enSynonym,
    'zhName' :zhName,
    'zhSynonym' : zhSynonym,
    'CBNumber' :CBNumber,
    'molecular' : molecular,
    'formula' : formula,
    'mofile' : mofile,
    'chemicalProperties': chemicalPropertiesObj
    }

#db is pymongo.db
cnt = 0
def SpiderCASIDList(entryURL, crawlAllPage, cbChemiInfoHandler):
    global baseHref, sleepDuration
    visitedURLs = set()
    unvisitedURLs = []
    logger.info( 'entryURL:'+ entryURL)
    pos = entryURL.rfind('/')
    baseHref, entryUrlPath = entryURL[:pos], entryURL[pos:]
    unvisitedURLs.append(entryUrlPath)

    def visitURL(targetURL):
        global cnt
        cnt = cnt+1

        logger.info('[cnt %s] begin visit url: '%str(cnt)+targetURL )

        timer = SleepTimer(GetSleepDuration())

        request = urllib2.urlopen(targetURL)
        content = request.read()
        request.close()
        content = content.decode(getEncoding(content))
        doc = html.document_fromstring(content)

        if crawlAllPage and cnt == 1:
            #all CAS names from 1->9
            all1to9 = doc.cssselect('td.detailLtd a')
            for alink in all1to9:
                href = alink.get('href')
                unvisitedURLs.insert(0, href)

        allOthersLinks = doc.cssselect('td[colspan="2"] a')[1:]
        logger.info( 'allOthersLinks: '+str( len(allOthersLinks) ) )
        for alink in allOthersLinks:
            href = alink.get('href')
            if href in visitedURLs:
                continue
            else:
                unvisitedURLs.insert(0, href)

        allCASLinks = doc.cssselect('td.style2 a')
        for i in xrange(0,len(allCASLinks),2):
            try:
                casDetailLink = allCASLinks[i].get('href')
                casDetailLink = '/'.join([baseHref, casDetailLink])
                #visit CAS detail
                cas = GetCASDetail(casDetailLink)
                if cbChemiInfoHandler:
                    cbChemiInfoHandler.process(cas)
            except Exception as err:
                logger.error('  visit cas URL %s failed'%casDetailLink)
                logger.error(str(err))
                errVisitPages.append(casDetailLink)


        logger.info( '[end visit cnt %s]  end visit url, visit cnt: '%str(cnt))
        timer.conditionSleep()


    while len(unvisitedURLs) > 0:
        urlPath = unvisitedURLs.pop()
        if urlPath in visitedURLs:
            continue

        if globalConfig['debugOpen'] and cnt > 0:
            break

        #visit this url and get html page
        targetURL = '/'.join([baseHref, urlPath])


        try:
            visitURL(targetURL)
        except Exception as err:
            logger.error('visitURL %s failed'%targetURL)
            logger.error(str(err))
            errVisitPages.append(targetURL)

    if len(errVisitPages) > 0:
        logger.error('All bad visit urls begin: ')
        for url in errVisitPages:
            logger.error(url)
        logger.error('End')

if __name__ == '__main__':
    GetCASDetail('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB4853677.htm')
