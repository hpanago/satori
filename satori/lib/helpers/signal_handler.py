import sys
import logging as log
import signal


def sigHandle(signal, frame) :
	print
	print "Aborted by the User..."
	sys.exit(0)

signal.signal( signal.SIGINT, sigHandle )


__log = log.getLogger( '__main__' )
__log.debug( 'Signal handler for SIGINT installed' )