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
pybforce -mode:0 [options] url
mode : 0,1,2 
        0 means trapping via regex, requires -regex option
        1, absolute timing attack, requires -time option
        2, dynamic timing attack, requires -time option
        3, trap http response status, requires -status option
url: the url to attack, by default the value $1 will be replaced with the bruteforce strings, another 
      repleace code can be specified via -replace
options:
  -time set the timeout to trap in seconds
  -regex set regular expreassion to trap
  -status set http response status to trap
  -replace specify another replace code placed in your url string
  -file: specify file to read with items to try
  -chars: specify characters to test
  -len: maximum length to test, default is 8
  -fixlen either 1 or 0 , 1 means only strings of length -len will be used, 0 means from length 1 to -len, default is 1
  -status 304
examples:
  pybforce -mode 3 -status 301 -chars 0123456789 -len 4 -fixlen 1 http://somehost/userauth.php?pincode=$1
  #scans for all permutations of 0-9 with a fixed length of 4 and traps the result via redirect
  pybfore -mode 0 -regex error -chars "</'{}&|@#" -length 1 http://someost/page.aspx?novalidation=$1
  # scans for special chars and traps the word error



  