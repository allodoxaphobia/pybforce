#!/usr/bin/env python

#----------------------------------
#pybforce.py
#Copyright R.Somers 2012
#----------------------------------

import sys
import urllib2
from threading import Thread
from optparse import OptionParser
import re



#GLOBAL VARS
PROGNAME="pybforce.py"
PROGVERSION="1.0"

MODE=0
REGEX=""
CHARSET=""
WORKLIST=[]
FILE=""
LENGTH=8
FIXLENGTH=1
URL=""
REPLACECODE="#1"

class Permutations():
    permlist=[]
    def get(self,prefix="",fixed_len=0):
        self.permuts(prefix,fixed_len)
        return self.permlist
    
    def __init__(self, charset, length):
        self.permlist=[]
        self.chars = charset.split(',')
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
    def __init__(self,engine,hit_regex, resp_status,resp_time):
        Thread.__init__(self)
        self.engine=engine
        self.regex= hit_regex
    
    def run(self):
        while 1:
            uri = self.engine.consumelastitem()
            if len(uri)> 0 :
		req= urllib2.urlopen(uri)
        	if re.match(self.regex,req.read()) != None:
			print uri
		else:
			print re.match(self.regex,req.read())
        	req.close()
            else: #empty worklist, let thread die and report back
                self.engine._threadsfinished=self.engine._threadsfinished+1
                return 0

#end class





class BruteForceEngine:
    _threadcount=100
    _threadsfinished=0
    _worklist=[]
    _bthreads=[]
    
    def __init__(self,result_regex="", result_status="", result_time=0):
        self._result_regex = result_regex
        self._result_status = result_status
        self._result_time = result_time
        for x in WORKLIST:
            self._worklist.append(URL.replace(REPLACECODE, x))
        
    def run(self):
        for threadcount in range(0,self._threadcount):
            self._bthreads.append(BFThread(self,self._result_regex,self._result_status,self._result_time))            
            self._bthreads[-1].start() #calls obj.run() on thread
        while self._threadsfinished < (self._threadcount-1): x=1 #wait for threads to exit
    
    #end def
    
    def consumelastitem(self):        
        try:
            x = self._worklist.pop()
            return x
        except:
            return ""


#end class





def setoptions(args):
    global WORKLIST, URL, MODE, REGEX, CHARSET, FILE, LENGTH,FIXLENGTH,REPLACECODE
    parser = OptionParser(usage=('type %s -help for usage' % PROGNAME), version=(PROGVERSION))
    parser.add_option("--mode", dest="MODE", default=0,
            help='Specify scanning mode 0,1,2 Default is 0' + '\n'
		+ '   0 : trap responses via regular expressions, requires the -regex option to be set \n'
		+ '   Mode 1 and 2 are not yet supported'
		)
    parser.add_option("--regex", dest="REGEX", default="", help="regular expression to look for in the result page")
    parser.add_option("--chars", dest="CHARSET", default="", help="Character set to use")
    parser.add_option("--file", dest="FILE", default="", help="load file of strings to test, if -chars is specified this setting will be ignored")
    parser.add_option("--len", dest="LENGTH", default=2, help="Maximum length of permutations made from characters in -char option")
    parser.add_option("--fixlen", dest="FIXLENGTH", default=1, help="set to 0try permutations with length 1 to -len, set to 1 to only try permutations of length -len")
    
    URL = args[-1] #should allways be the last in line
    (options, parsedargs) = parser.parse_args(args)
    MODE = options.MODE
    REGEX = options.REGEX
    CHARSET = options.CHARSET
    FILE = options.FILE
    LENGTH= options.LENGTH
    FIXLENGTH = options.FIXLENGTH
    
    if MODE == 0:
	if REGEX== "":
		print "Can't run in regex matching mode without --regex option"
		return 0
    if CHARSET != "":
    	tmp = Permutations(CHARSET,LENGTH)
	WORKLIST= tmp.get("",FIXLENGTH) #todo: add support for prefixes and suffixes
    else:
	if FILE != "":
		print "FILE mode not yet supported, using pincode settings"
		#TODO: actually load a file
		#below is for testing
	    	tmp = Permutations("012345678",4)
		WORKLIST= tmp.get("",FIXLENGTH)
	else:
		#no harset and no file? => abort
		print "Please specify either a charset or a file "
		return 0
    return 1

if __name__ == "__main__":
    if setoptions(sys.argv[1:]) == 1:
	    bf = BruteForceEngine(REGEX,"","")
	    bf.run()





