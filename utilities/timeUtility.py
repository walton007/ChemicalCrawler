import time
from logger import GetLogger
logger = GetLogger()

class SleepTimer(object):
    def __init__(self, sleepSeconds):
        self.starttime = time.clock()
        self.sleepSeconds = sleepSeconds


    def conditionSleep(self):
        endtime = time.clock()
        elapsed = endtime - self.starttime
        if elapsed < self.sleepSeconds:
            sleepDuration = self.sleepSeconds - elapsed
            logger.info('sleep for %s seconds'%str(sleepDuration))
            time.sleep(sleepDuration)
