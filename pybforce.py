#!/usr/bin/env python

#----------------------------------
#pybforce.py
#Copyright R.Somers 2012
#----------------------------------

import urllib2
from threading import Thread
from time import sleep


class Permutations():
    permlist=[]
    def get(self,prefix="",fixed_len=0):
        self.permuts(prefix,fixed_len)
        return self.permlist
    
    def __init__(self, charset, length):
        self.permlist=[]
        self.chars = charset.split(",")
        self.length=length
        
    def permuts(self,prefix="",fixed_len=0):
        for char in self.chars:
            if (len(prefix)+1 < self.length):
                self.permuts(prefix+char, fixed_len)
                if (fixed_len==0):
                    self.permlist.append(prefix + char)
            else:
               self.permlist.append(prefix + char)
    
    #end def

#end class





class BFThread(Thread):
    def __init__(self,engine,hit_regex=""):
        Thread.__init__(self)
        self.engine=engine
        self.regex= hit_regex
    
    def run(self):
        while 1:
            uri = self.engine.consumelastitem()
            if len(uri)> 0 :
                req= urllib2.urlopen(uri)
                if req.getcode()==200:
                    print req.read()
                req.close()
            else: #empty worklist, let thread die and report back
                self.engine._threadsfinished=self.engine._threadsfinished+1
                return 0

#end class





class BruteForceEngine:
    _threadcount=100
    _threadsfinished=0
    _baseuri = ""
    _replacecode=""
    _permset=[]
    _worklist=[]
    _result_regex=""
    _bthreads=[]
    
    def __init__(self,baseuri,replacecode,permset,result_regex=""):
        self._baseuri = baseuri
        self._replacecode = replacecode
        self._permset = permset
        self._result_regex = result_regex

    def run(self):
        for x in self._permset:
            self._worklist.append(self._baseuri.replace(self._replacecode, x))
        
        self._permset=[] #free mem
        print "threading"
        for threadcount in range(0,self._threadcount):
            self._bthreads.append(BFThread(self,self._result_regex))            
            self._bthreads[-1].start() #calls obj.run() on thread
        print "threads loaded"
        while self._threadsfinished < (self._threadcount-1): x=1 #wait for threads to exit
            
        print "done"

    def consumelastitem(self):        
        try:
            x = self._worklist.pop()
            return x
        except:
            return ""


#end class

if __name__ == "__main__":
    perms = Permutations("0,1,2,3,4,5,6,7,8,9",9)
    fx= perms.get("015226", 0)
    bf = BruteForceEngine("http://armepc36?q=$1","$1",fx,"")
    bf.run()
