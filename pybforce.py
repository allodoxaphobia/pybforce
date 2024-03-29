#!/usr/bin/env python

import sys
from pybforce import Worklist
from pybforce import Engine
from pybforce import ResultTrapMode
from optparse import OptionParser

PROGNAME="pybforce.py"
PROGVERSION="1.0"

MODE = 0
PARAM = ""
ENGINE= None

def setoptions(args):
    global MODE, PARAM, ENGINE
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
    parser.add_option("-p", dest="PARAM", default="", help="Parameter field depens on mode, either regular expression, http response code or time in seconds")
    parser.add_option("-c", dest="CHARS", default="", help="Character set to use")
    parser.add_option("-f", dest="FILE", default="", help="load file of strings to test, if -chars is specified this setting will be ignored")
    parser.add_option("-l", dest="LENGTH", type="int", default=0, help="Maximum length of permutations made from characters in -char option")
    parser.add_option("-x", dest="FIX", default=1, help="set to 0try permutations with length 1 to -len, set to 1 to only try permutations of length -len")
    parser.add_option("-e", dest="EXIT", default="1", help="Stop scanning when a match is found default is 1, set to 0 to continue scanning")
    parser.add_option("-t", dest="THREADS", default="750", help="Number of concurrent threads/connections to use.")

    if len(args) == 0:
        print 'Usage: ' + parser.usage
        return 0
    
    (options, parsedargs) = parser.parse_args(args)
    
    url = args[-1]
    worklist = None
    
    if (options.CHARS== "" and options.FILE=="") :
        #no charset and no file? => abort
        print "Error: Please specify either a charset or a file "
        print 'Usage: ' + parser.usage		
        return 0
    else:
        if (options.CHARS !=""):
            if (options.LENGTH==0):
                print "Error: No maximum lenght specified (-l option)"
                print 'Usage: ' + parser.usage	
                return 0
    MODE = options.MODE
    PARAM = options.PARAM
    if (PARAM==""):
        print "No parameter specified (option -p), this option is required"
        print 'Usage: ' + parser.usage
        return 0
    if (options.CHARS != ""):
        worklist = Worklist(options.CHARS)
        worklist.generate("",options.LENGTH,url,"#1", int(options.FIX))
    if (options.FILE != ""):
        worklist = Worklist("")
        worklist.loadfromfile(options.FILE,url)

    ENGINE = Engine(worklist._items,int(options.THREADS), int(options.EXIT))
    return 1

if __name__ == "__main__":
    if setoptions(sys.argv[1:]) == 1:
            ENGINE.run(MODE,PARAM)
