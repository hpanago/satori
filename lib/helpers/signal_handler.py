import sys

import signal

def sigHandle(a, b) :
	print "Aborted by the User..."
	sys.exit(0)

signal.signal( signal.SIGINT, sigHandle )