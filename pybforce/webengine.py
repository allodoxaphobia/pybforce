from bfthread import WebThread
from time import sleep
from shared import ScanTime

class Engine():
    _exitonhit=1
    _threadcount=0
    _runningthreads=0
    _worklist= []
    _thread_container=[]
    _killbit=0
    _scan_mode=0
    _scan_param=""
    _verbose=1
    
    def __init__(self, lworklist, thread_count=0,exit_on_hit=1):
        if len(lworklist) >0 :
            self._worklist=lworklist
            self._exitonhit=exit_on_hit
            self._threadcount = thread_count
            if len(lworklist) < thread_count: self._threadcount= len(lworklist)
    
    def run(self, mode, param, verbose=1):
        self._scan_mode=mode
        self._scan_param=param
        self._verbose=verbose
        try:
            if (verbose>=1): print ScanTime() + " Scan started, using " + str(self._threadcount) + " threads"
            for threaditem in range(0,self._threadcount):
                self._thread_container.append(WebThread(self))
                self._runningthreads=self._runningthreads+1
                self._thread_container[-1].start()
            while self._runningthreads>0:
                if (self._killbit==1):
                    self.die()
                    break
            if (verbose>=1):  print ScanTime() + " Scan finished"
            
        except KeyboardInterrupt:
            if (self._verbose>0): print ScanTime() + " Scan cancelled by user, killing threads"
            self.die()
    
    def die(self):
        try:
            self._killbit=1
            sleep(2)
        except KeyboardInterrupt:
            print "Forcfully terminated by user"
    
    def consumelastitem(self):
        try:
            if len(self._worklist)> 0:
                return self._worklist.pop()
            else:
                return None
        except: #race condition: last item just popped by other thread
            return None
