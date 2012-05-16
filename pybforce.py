#!/usr/bin/env python

############################################
#               pybforce.py                #
#         Copyright R.Somers 2012          #
############################################

import sys
import urllib2
from threading import Thread
from optparse import OptionParser
import re
import socket
#from time import sleep
from math import pow

############################################
#                GLOBAL VARS               #
############################################

PROGNAME="pybforce.py"
PROGVERSION="1.0"

MODE=0
PARAM=""
CHARSET=""
WORKLIST=[]
FILE=""
LENGTH=8
FIXLENGTH=1
URL=""
REPLACECODE="#1"
EXITONHIT=1


############################################
#          Class Permutations              #
############################################

class Permutations():
    permlist=[]
    def get(self,prefix="",fixed_len=0):
        self.permuts(prefix,fixed_len)
        return self.permlist
    
    def __init__(self, charset, length):
        self.permlist=[]
        self.chars = charset
        self.length=length
    
    def permuts(self,prefix="",fixed_len=0):
        for char in self.chars:
            if (len(prefix)+1 < self.length):
                self.permuts(prefix+char, fixed_len)
                if (fixed_len==0):
                    self.permlist.append(prefix + char)
            else:
                self.permlist.append(prefix + char)

#end class



############################################
#          Class BFThread                  #
############################################

class BFThread(Thread):
    def __init__(self,engine):
        Thread.__init__(self)
        self.engine=engine
    
    def run(self):
        while 1:
            if self.engine._killbit==1: return 0
            uri = self.engine.consumelastitem()
            if len(uri)> 0 :            
                if self.engine._mode==0: #TRAPPING VIA REGEX
                    req= urllib2.urlopen(uri)
                    if re.search(self.engine._param,req.read()) != None:
                        print "REGEX MATCH ON " + uri
                        self.engine._killbit=self.engine._exitonhit
                    req.close()
                elif self.engine._mode==1: #TRAPPING ON STATUS
                    try:
                        req= urllib2.urlopen(uri)
                        print "STATUS MATCH ON " + uri
                        self.engine._killbit=self.engine._exitonhit
                        req.close()
                    except urllib2.HTTPError, e: #TRAPPING VIA HTTP STATUS
                        if self.engine._mode==1 and self.engine._param == str(e.code):
                            print "STATUS MATCH ON " + uri
                            self.engine._killbit=self.engine._exitonhit
                elif self.engine._mode==2:
                    try:
                        req= urllib2.urlopen(uri, timeout= int(self.engine._param))
                        req.close()
                    except socket.timeout:
                        print "TIMEOUT MATCH ON " + uri + '\n'
                        self.engine._killbit=self.engine._exitonhit
            else:
                #empty worklist, let thread die and report back
                self.engine._threadsfinished= self.engine._threadsfinished+1
                return 0
        self.engine._threadsfinished= self.engine._threadsfinished+1
        return 0

#end class



############################################
#       Class BruteForceEngine             #
############################################

class BruteForceEngine:
    _threadcount=750  #default, for timing mode this will be set to 250
    _threadsfinished=0
    _worklist=[]
    _bthreads=[]
    _killbit=0
    _param=""
    _mode=0
    
    def __init__(self,mode=0,param="", exitonhit=1):
        self._param = param
        self._mode= mode
        self._exitonhit=exitonhit
        if mode ==2: self._threadcount=250 #must be carefull not to throttle the server during timing attacks
        for x in WORKLIST:
            self._worklist.append(URL.replace(REPLACECODE, x))
    
    def run(self):
        try:
            print "# Starting engine on " + str(self._threadcount) + " threads."
            for threadcount in range(0,self._threadcount):
                self._bthreads.append(BFThread(self))            
                self._bthreads[-1].start() #calls obj.run() on thread
            while self._threadsfinished < (self._threadcount-1):
                if self._killbit==1: return 0 #wait for threads to exit
        except KeyboardInterrupt:
            self._killbit=1
    
    #end def
    
    def consumelastitem(self):        
        try:
            x = self._worklist.pop()
            return x
        except:
            return ""


#end class



############################################
#             Class Main                   #
############################################

def setoptions(args):
    global WORKLIST, URL, MODE, PARAM, CHARSET, FILE, LENGTH,FIXLENGTH,REPLACECODE, EXITONHIT
    parser = OptionParser(usage=(PROGNAME + ' [options] url'
                                    + '\n       type ' + PROGNAME + ' -h for options'                                 
                                 ), version=(PROGVERSION))
    parser.add_option("-m", type="int",dest="MODE", default=0,
            help='Specify scanning mode 0,1,2,3 Default is 0'
            + ' 0 : trap responses via regular expressions, requires the -reg option to be set'
            + ' 1 : trap responses via response statusr, requires the -s option to be set (default is 200), useful for url guessing or session bruteforcing'
            + ' 2 : trap requests by timeouts, useful for blind sql timing attacks'
            + ' 3 : relative timing, to compensate for server load: not yet implemented'
            )
    parser.add_option("-r", dest="REGEX", default="", help="regular expression to look for in the result page")
    parser.add_option("-c", dest="CHARS", default="", help="Character set to use")
    parser.add_option("-f", dest="FILE", default="", help="load file of strings to test, if -chars is specified this setting will be ignored")
    parser.add_option("-l", dest="LENGTH", type="int", default=2, help="Maximum length of permutations made from characters in -char option")
    parser.add_option("-x", dest="FIX", default=1, help="set to 0try permutations with length 1 to -len, set to 1 to only try permutations of length -len")
    parser.add_option("-s", dest="STATUS", default="200", help="http response status to trap")
    parser.add_option("-t", dest="TIME", default="5", help="request time treshhold, use thos for mode 2 to trap requests taking langer then x seconds, usefull for blind sqli timing attacks")
    parser.add_option("-e", dest="EXIT", default="1", help="Stop scanning when a match is found default is 1, set to 0 to continue scanning")


    if len(args) == 0:
        print 'Usage: ' + parser.usage
        return 0
    
    (options, parsedargs) = parser.parse_args(args)
    
    URL = args[-1]
    
    MODE = options.MODE
    if MODE == 0:
        PARAM = options.REGEX
        if PARAM == "":
            print "Error: Can't run in regex matching mode without -r option"
            print 'Usage: ' + parser.usage
	    return 0            
    elif MODE == 1:
        PARAM = options.STATUS
    elif MODE == 2:
        PARAM= options.TIME
    else:
        print "Error: This mode is not supported"
        print 'Usage: ' + parser.usage
        return 0
    
    CHARSET = list(options.CHARS)
    FILE = options.FILE
    LENGTH= options.LENGTH
    FIXLENGTH = options.FIX
    STATUS = str(options.STATUS)
    EXITONHIT= int(options.EXIT)

    if len(CHARSET) != 0:
        print "# Computing permutations, this might take a while..."
    	tmp = Permutations(CHARSET,LENGTH)
	WORKLIST= tmp.get("",FIXLENGTH) #todo: add support for prefixes and suffixes
    else:
	if FILE != "":
            try:
                f = open(FILE,"r")
                fdata = f.read().split("\n")
                for line in fdata:
                    if line != "": WORKLIST.append(line)
            except:
                print "Error reading file : " + FILE + " aborting."
                return 0 
	else:
		#no charset and no file? => abort
		print "Error: Please specify either a charset or a file "
                print 'Usage: ' + parser.usage		
		return 0
    return 1

#end def

if __name__ == "__main__":
    if setoptions(sys.argv[1:]) == 1:
            bf = BruteForceEngine(MODE,PARAM, EXITONHIT)
            bf.run()



