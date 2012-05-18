import urllib2
from threading import Thread
import re
from shared import ResultTrapMode, ScanTime
import socket

class WebThread(Thread):
    _engine= None
    def __init__(self,parent_engine):
        self._engine = parent_engine
        Thread.__init__(self)
    
    def run(self):
        while 1:
            if self._engine._killbit==1:
                self.die()
                return 0
            uri = self._engine.consumelastitem()
            if uri == None:
                self.die()
                return 0
            else:
                if (self._engine._scan_mode==ResultTrapMode.regex): self.scanregex(uri)
                elif (self._engine._scan_mode==ResultTrapMode.status): self.scanstatus(uri)
                elif (self._engine._scan_mode==ResultTrapMode.absolutetime): self.scantime(uri)
                else: self.die()
        return 0

    def scanregex(self,url):
        req = urllib2.urlopen(url, timeout= 20)
        if (re.search(self._engine. _scan_param,req.read()) != None):
                     print ScanTime() + " REGEX_HIT: " +url
                     self._engine._killbit=self._engine._exitonhit
        req.close()

    def scanstatus(self,url):
        try:
            req = urllib2.urlopen(url, timeout= 20)
            if self._engine._scan_param=="200":
                     print ScanTime() + " STATUS_HIT: " + url
                     self._engine._killbit=self._engine._exitonhit
            req.close()
        except urllib2.HTTPError, e:
            if self._engine._scan_param == str(e.code):
                     print ScanTime() + " STATUS_HIT: " + url
                     self._engine._killbit=self._engine._exitonhit

    def scantime(self,url):
        try:
            req = urllib2.urlopen(url, timeout= int(self._engine._scan_param))
            req.close()
        except socket.timeout:
            print ScanTime() + " TIMER_HIT: " + url
            self._engine._killbit=self._engine._exitonhit
    
    def die(self):
        self._engine._runningthreads = self._engine._runningthreads-1
