import urllib2
from lxml import html
from utilities.utilities import getEncoding
from utilities.logger import GetLogger
from utilities.timeUtility import SleepTimer
from model.chemiInfo import ChemiInfo
from model.chemiDetailInfo import *

logger = GetLogger()

#db is pymongo.db
cnt = 0
constBaseURL = 'http://www.chemicalbook.com/'
def GetChemiDetailInfo(chemiDetailURL):
    content = urllib2.urlopen(chemiDetailURL).read()
    content = content.decode(getEncoding(content))
    doc = html.document_fromstring(content)
    ProductIntroduction = doc.cssselect('#ProductIntroduction table[border="0"]')[0]
    ChemicalProperties = doc.cssselect('#ChemicalProperties')[0]
    SafetyInformation = doc.cssselect('#SafetyInformation')[0]
    #parse ProductIntroduction
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
    mofile = urllib2.urlopen('/'.join([constBaseURL, mofilelink])).read()
    mofile = mofile.decode(getEncoding(mofile))

    #parse chemicalProperty
    chemicalProperty = None
    try:
        rongdian = ChemicalProperties.cssselect('#ChemicalProperties__ctl0_PropertyValueLabel')[0].text
        feidian = ChemicalProperties.cssselect('#ChemicalProperties__ctl1_PropertyValueLabel')[0].text         
        shandian = ChemicalProperties.cssselect('#ChemicalProperties__ctl2_PropertyValueLabel')[0].text   
        CASLink = ChemicalProperties.cssselect('#ChemicalProperties__ctl7_PropertyValueLabel a')[0].get('href')
        chemicalProperty = ChemicalProperty(rongdian, feidian, shandian, CASLink, None, None)
    except Exception as err:
        logger.error('parse chemicalProperty error@ chemiDetailURL: %s'%chemiDetailURL)
        logger.error(str(err))



    #parse chemicalSecurityInfo
    securityInfo = None
    try:
        securityLevelLink = SafetyInformation.cssselect('#SafetyInformation__ctl1_PropertyValueLabel a')[0].text
        securityNoteLink = SafetyInformation.cssselect('#SafetyInformation__ctl2_PropertyValueLabel a')[0].text
        transferID = SafetyInformation.cssselect('#SafetyInformation__ctl3_PropertyValueLabel')[0].text
        securityInfo = ChemicalSecurityInfo(securityLevelLink, securityNoteLink, transferID)
    except Exception as err:
        logger.error('parse ChemicalSecurityInfo error@ chemiDetailURL: %s'%chemiDetailURL)
        logger.error(str(err))

    detailInfo = ChemiDetailInfo(CAS, enName, enSynonym, zhName, zhSynonym, CBNumber, formula , molecular ,
        mofile, chemicalProperty, securityInfo)

    return detailInfo


def SpiderCASDetailList(entryURL, cbChemiInfoHandler):
    print 2
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

        if cnt > 2:
            logger.warn( 'Early Return')
            return

        content = urllib2.urlopen(targetURL).read()
        content = content.decode(getEncoding(content))
        doc = html.document_fromstring(content)

        alltrs = doc.cssselect('table tr')
        if len(alltrs) == 0:
            return

        for tr in alltrs[1:]:
            tds = tr.cssselect('td')
            casElem, zhNameElem, enNameElem, mfElem = tds
            #get CAS and CASLink
            alink = casElem.cssselect('a')[0]
            caslink = alink.get('href')
            cas = alink.text

            #get enName and enNameLink
            alink = zhNameElem.cssselect('a')[0]
            zhNameLink = alink.get('href')
            zhName = alink.text

            #get enName
            enName = enNameElem.text

            #get mf
            mf = mfElem.cssselect('span')[0].text

            chemInfo = ChemiInfo(enName, zhName, None, zhNameLink, cas, caslink, mf)
            fullLink = '/'.join([baseHref, zhNameLink])

            try:
                chemiDetailInfo = GetChemiDetailInfo(fullLink)
                chemInfo['chemiDetailInfo']= chemiDetailInfo
            except Exception as err:
                logger.error('parse GetChemiDetailInfo error@ chemiDetailURL: %s'%fullLink)
                logger.error(str(err))

            if cbChemiInfoHandler:
                cbChemiInfoHandler.process(chemInfo)

            #detail info handling

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


def GetInfoFromCASLink(href):
    return None

def GetInfoFromZHNameLink(href):
    return None

if __name__ == '__main__':
    print 'SpiderProductCASDetailList'
    GetChemiDetailInfo('http://www.chemicalbook.com/ChemicalProductProperty_CN_CB2854357.htm')
