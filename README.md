pybforce
========

little command line bruteforcer in python

pybforce is a multi threaded get request scan tools for webpages that (will) support(s) the following:
-bruteforcing with internal generator
-bruteforcing with a list of items (textfile)

Trapping of possitive result occurs by:
- matching regex expressions in the page output: your average password bruteforcing
- matching via response status: for bruteforcing with redirects, or trapping server errors (fuzzing)
- matching via timing: this is useful for blind sql timing attacks. it will support absolute timeouts as well 
  as dynamic timeouts, this to accomodate timing attacks based on server load (to atchieve this before every request
  a benchmarking request wuill be made)


usage:
------

pybforce [options] url


options
--------

-m 	mode : 0,1,2 default is 0
        0 means trapping via regex, requires -p option to be set to a regular expression
        1, trap http response codes, requires -p option to be set to a http response status code
        2, trap response times, requires requires -p option to be set to a interval in seconds, this setting will then be used for the socket timeout
        3, trap dynamic response times, not yet implemented
-p	mode parameter, either a regular expression, a http response code or a time interval in seconds
-c	character set: characters to use in permutations
-l	maximum length of permutations
-x	pemrutations have a fixed length (value of -l)
-f	use this to load a files with a list of values (each value on seperate line), this can be used in stead of the -r option
-t	threads, number of threads/connections to use, default is 750
-e	set to 0 if you want to keep scanning after a match is found, default is   1, meaning the scanner will stop if a match is found


url
----
the url to use, by default the value #1 will be replaced with the bruteforce strings. Currently there is no option to change the replace code

examples:
---------
  example 1: pin code bruteforcing
  scan for all permutations of 0-9 with a fixed length of 4 and will result in a hit if the word success is found on the page
  option -e  is ommited, the default is 1, this example will stop when a matching page is found
  # pybforce.py -c "0123456789" -l -x 1 -p "^success" http://www.targetserver.net/login.php?pincdoe=#1

  example 2: url bruteforcer
  this example scans a directory for mfilenames with extentiion .jpg and matches the resulting http 200 response status
  # pybforce.py -m 1 -p 200 -c "0123456789ABCDEF" -l 12 -x 1 http://somehost/images/#1.jpg




  
