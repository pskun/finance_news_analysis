# encoding=utf-8

import sys
import urllib2

if len(sys.argv) != 2:
    print "Usage: python %s url > output.html" % sys.argv[0]
    sys.exit(1)

url = sys.argv[1]

response = urllib2.urlopen(url)
html = response.read()
print html  