#!/usr/bin/python
#-*- coding: utf-8 -*-

import platform as plat
import sys
import logging as log
import argparse

import lib.image_differ as differ
import lib.image_io as io
import lib.definitions as defs

import lib.helpers.signal_handler

header = defs.header.format( "OS filesystem image Difference Finder" )

# log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



def main():

	parser = argparse.ArgumentParser( description = 'Deeply diffs 2 satori Images' )

	parser.add_argument( 'original', help = "Satori image to be treated as 'original'", type = str )
	parser.add_argument( 'subject', help = "Satori image to be examined", type = str )

	parser.add_argument( 'directory', help = 'Filesystem directory to start the diffing',\
										type = str, default = '/' )

	parser.add_argument( '--type', '-t', help = 'Choose the file type of the images saved/loaded',\
										type = str, choices = ['pickle', 'json', 'sqlite'], default = 'json')

	parser.add_argument( '--no-gzip', '-ng', help = 'Image IO will *NOT* use gzip', action = 'store_true', default = False)

	verb = parser.add_mutually_exclusive_group()
	verb.add_argument( '-v', '--verbose' , help = 'verbose mode', action = 'count', default = 0 )
	verb.add_argument( '--debug' , '-d', help = 'debugging mode', action = 'store_true', default = False )
	verb.add_argument( '--quiet', '-q' , help = 'quiet mode (show only critical differences)', action = 'store_true', default = False )

	# out = parser.add_mutually_exclusive_group()
	# out.add_argument( '--tree', help = 'Prints a "git-flavoured" Diff Tree for the Filesystems (/dev/stderr)', action = 'store_true', default = False )
	# out.add_argument( '--log', help = 'Prints a "greppable" log of the Differences for the Filesystems (/dev/stdout)', action = 'store_true', default = True )
	# out.add_argument( '--all', help = 'Prints both a log (/dev/stdout) and a Diff Tree (dev/stderr)', action = 'store_true', default = False )


	args = parser.parse_args()



	'''	================================================ VERBOSITY CHECKS ================================================ '''

	if args.debug :
		__log.setLevel( log.DEBUG )
		
	elif args.quiet :
		__log.setLevel( log.ERROR )

	elif args.verbose == 0 :
		__log.setLevel( log.WARNING )

	elif args.verbose == 1 :
		__log.setLevel( log.INFO )



	'''	================================================ HEADER + INFO ================================================ '''

	__log.info(header)

	if args.debug :
		__log.debug("* Debugging mode *")
	else :
		__log.warning("Verbosity set to: %d" % args.verbose)



	'''	================================================ COMPRESSION OPTION ================================================ '''

	if args.no_gzip :
		__log.info( "* Compression is Disabled! *" )
	else :
		__log.info( "Compression is Enabled!" )
		io.__use_gzip = True


	root_dir = args.directory
	__log.info( "Diffing will traverse the '%s' directory" % root_dir )


	image1 = io.loadImage( args.original, args.type )
	if not image1 :
		__log.critical( defs.cant_read_file % args.original )
		sys.exit(-1)

	image2 = io.loadImage( args.subject, args.type )
	if not image2 :
		__log.critical( defs.cant_read_file % args.subject )
		sys.exit(-1)



	differ.diffSystem( image1, image2, root_dir )
	__log.warning( "\n" )

if __name__ == "__main__" :
    
    main()
