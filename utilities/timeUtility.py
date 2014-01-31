import time

class SleepTimer(object):
    def __init__(self):
        self.starttime = time.clock()

    def conditionSleep(self):
        endtime = time.clock()
        elapsed = endtime - self.starttime
        if elapsed < 5:
            sleepDuration = 5 - elapsed
            print 'sleep for %s seconds'%str(sleepDuration)
            time.sleep(sleepDuration)
