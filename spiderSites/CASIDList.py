from myConfig import GetSleepDuration, GetGlobalConfig, GetWaitDuration
globalConfig = GetGlobalConfig()

import myexcept
from myexcept.myException import ReadURLException
import urllib2
import socket

# curl -x http://127.0.0.1:51984 http://www.chemicalbook.com/ShowAllProductByIndexID_CAS_12_0.htm
socket.setdefaulttimeout(50)

from utilities.proxy import SwitchProxy

if len(globalConfig['httpProxy']) > 7:
    SwitchProxy()


from lxml import html
from bs4 import BeautifulSoup

from utilities.utilities import getEncoding
from utilities.logger import GetLogger, GetHtmlLogger
from utilities.timeUtility import SleepTimer

logger = GetLogger()
htmllogger = GetHtmlLogger()
baseHref = 'http://www.chemicalbook.com'
errVisitPages = []

from db.statUtil import StatisticHelper
gStatisticHelper = StatisticHelper(globalConfig['dbstSchema'])

def GetCASDetail(casURL):
    logger.info('  begin get CASDetail:'+casURL)
    timer = SleepTimer(GetSleepDuration())

    tryCnts = 1
    while True:
        try:
            request = urllib2.urlopen(casURL)
            content = request.read()
            request.close()
            format = getEncoding(content)
            content = content.decode(format)
            soup = BeautifulSoup(content)
            doc = html.document_fromstring(soup.prettify())

            #parse ProductIntroduction
            cssList = doc.cssselect('#ProductIntroduction table[border="0"]')
            if len(cssList) == 0:
                logger.error('#ProductIntroduction table[border="0"] failed')
            ProductIntroduction = cssList[0]

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
            filecodec = getEncoding(mofile)
            if filecodec is not None:
                try:
                    mofile = mofile.decode(filecodec)
                except Exception as errDecode:
                    logger.warn('decode mofile fail %s err:%s'%('/'.join([baseHref, mofilelink]), errDecode))

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

            #success pass
            break

        except Exception as err:
            tryCnts = tryCnts+1
            if tryCnts > 10:
                raise ReadURLException("can't open url %s"%casURL)

            logger.warn('  get CAS Detail Not success: %s'%casURL)
            logger.info('  try get for %s time'%tryCnts)
            SwitchProxy()
            continue

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
initialized = False
def SpiderCASIDList(entryURL, crawlAllPage, cbChemiInfoHandler):
    global baseHref, sleepDuration
    visitedURLs = set()
    unvisitedURLs = []
    logger.info( 'entryURL:'+ entryURL)
    pos = entryURL.rfind('/')
    baseHref, entryUrlPath = entryURL[:pos], entryURL[pos:]
    unvisitedURLs.append(entryUrlPath)

    def visitURL(targetURL):
        global cnt, initialized
        cnt = cnt+1

        logger.info('[cnt %s] begin visit url: '%str(cnt)+targetURL )

        timer = SleepTimer(GetSleepDuration())
        request = urllib2.urlopen(targetURL)
        content = request.read()
        request.close()
        content = content.decode(getEncoding(content))
        soup = BeautifulSoup(content)
        doc = html.document_fromstring(soup.prettify())

        #if no all other links, means serve have block this ip
        allOthersLinks = doc.cssselect('td[colspan="2"] a')[1:]
        logger.info( 'allOthersLinks: '+str( len(allOthersLinks) ) )
        if len(allOthersLinks) == 0:
            return 'tryAgain'

        #check first, if there's no cas content here, means there's no need to furthure on
        allCASLinks = doc.cssselect('td.style2 a')
        if len(allCASLinks) == 0:
            #early return
            logger.warn( '[end visit cnt %s]  end visit url, early return because no cas found in this page '%str(cnt))
            htmllogger.info('[] visit %s found no cas records'%targetURL)
            htmllogger.info(content)

            timer.conditionSleep()
            return 'nodata'

        logger.info( 'this page contains cas count: %s', len(allCASLinks)/2)
        for alink in allOthersLinks:
            href = alink.get('href')
            if href in visitedURLs:
                continue
            else:
                unvisitedURLs.insert(0, href)


        for i in xrange(0,len(allCASLinks),2):
            try:
                casDetailLink = allCASLinks[i].get('href')
                casDetailLink = '/'.join([baseHref, casDetailLink])

                #if visited then ignore
                if gStatisticHelper.isUrlVisited(casDetailLink):
                    logger.info(' %s already visited, so skip it'%casDetailLink)
                    continue

                #visit CAS detail
                cas = GetCASDetail(casDetailLink)
                gStatisticHelper.markUrlVisited(casDetailLink)
                if cbChemiInfoHandler:
                    cbChemiInfoHandler.process(cas)
            except Exception as err:
                logger.error('  visit cas URL %s failed'%casDetailLink)
                logger.error(str(err))
                errVisitPages.append(casDetailLink)


        if crawlAllPage and not initialized:
            #all CAS names from 1->9
            all1to9 = doc.cssselect('td.detailLtd a')
            for alink in all1to9:
                href = alink.get('href')
                unvisitedURLs.insert(0, href)
            initialized = True

        logger.info( '[end visit cnt %s]  end visit url, visit cnt: '%str(cnt))
        timer.conditionSleep()
        return 'ok'


    while len(unvisitedURLs) > 0:
        urlPath = unvisitedURLs.pop()
        if urlPath in visitedURLs:
            continue

        if globalConfig['debugOpen'] and cnt > 0:
            break

        #visit this url and get html page
        targetURL = '/'.join([baseHref, urlPath])


        try:
            tryTimeCnt = 0
            while True:
                retVal = visitURL(targetURL)
                if 'ok' == retVal:
                    tryTimeCnt = 0
                    break
                elif 'nodata' == retVal:
                    logger.info('encounter nodata url:'%targetURL)
                    break
                elif 'tryAgain' == retVal:
                    tryTimeCnt = tryTimeCnt + 1
                    if tryTimeCnt > 10:
                        tryTimeCnt = 0
                        logger.warn(' try to visit more than 10 time for url %s, so give up...'%targetURL)
                        break
                    else:
                        SwitchProxy()
                        #Sleep for some time
                        seconds = GetWaitDuration()
                        SleepTimer(seconds).conditionSleep()
                        continue

        except Exception as err:
            logger.error('visit CasCatogory URL %s failed'%targetURL)
            logger.error(str(err))
            errVisitPages.append(targetURL)

    if len(errVisitPages) > 0:
        logger.error('All bad visit urls begin: ')
        for url in errVisitPages:
            logger.error(url)
            gStatisticHelper.markUrlBadVisited(url)
        logger.error('End')



def testGetCASDetail():
    GetCASDetail('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB8417130.htm')
    GetCASDetail('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB3948424.htm')


if __name__ == '__main__':
    testGetCASDetail()
