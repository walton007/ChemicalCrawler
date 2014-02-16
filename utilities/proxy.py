import urllib2
from logger import GetLogger

logger = GetLogger()

def installProxy(proxy):
    logger.info('install proxy: %s'%proxy)
    proxy_support = urllib2.ProxyHandler({'http': proxy})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

from myConfig import GetSleepDuration, GetGlobalConfig, GetWaitDuration

#global variables
currentProxyIdx = -1
proxyList = []

def InitProxyConf():
    global proxyList
    globalConfig = GetGlobalConfig()
    httpProxyList = globalConfig['httpProxy']
    if len(httpProxyList) > 7:
        proxyList = httpProxyList.split(';')

InitProxyConf()

def SwitchProxy():
    global currentProxyIdx
    if len(proxyList) > 0:
        logger.info('switch proxy')
        currentProxyIdx = (currentProxyIdx+1) % len(proxyList)
        installProxy(proxyList[currentProxyIdx])
    else:
        logger.info('no proxy to switch')
