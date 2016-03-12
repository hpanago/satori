#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import platform as plat

import logging as log
import argparse

import lib.image_maker as maker
import lib.image_differ as differ
import lib.image_io as io
import lib.image_meta as meta


import curses  # Get the module

import atexit


header = '''
Welcome to Satori (悟り)
OS filesystem image creator and difference finder
Version {0}
'''.format(meta.version)

# @atexit.register
# def goodbye():
#     """ Reset terminal from curses mode on exit """
#     curses.nocbreak()
#     if stdscr:
#         stdscr.keypad(0)
#     curses.echo()
#     curses.endwin()


log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )

if __name__ == "__main__" :
	os_def_name = plat.platform()
	parser = argparse.ArgumentParser( prog = sys.argv[0], description = 'Diffs file system images of a live OSs with ones of fresh installation' )

	utility = parser.add_mutually_exclusive_group()
	utility.add_argument( '--image', help = 'Create an image file named "IMAGE"', default = '{0}.pkl'.format(os_def_name) )

	utility.add_argument( '--diff', help = 'Diff two filesystem images', nargs = 2, type = str, metavar = 'IMAGE' )

	data_type = parser.add_mutually_exclusive_group()
	data_type.add_argument( '--json', '-j', help = 'Image file is of JSON format', action = 'store_true' )
	data_type.add_argument( '--pickle', '-p', help = 'Image file is a python pickle', action = 'store_true' )
	data_type.add_argument( '--db', help = 'Image file is an sqlite db', action = 'store_true' )

	parser.add_argument( '--default-name', '-d', help = 'Just print the default filename for this machine and exit', action = 'store_true' )

	verb = parser.add_mutually_exclusive_group()
	verb.add_argument( '-v', '--verbose' , help = 'verbose mode', action = 'count', default = 0 )
	verb.add_argument( '--debug' , help = 'debugging mode', action = 'store_true', default = False )

	args = parser.parse_args()

	exten = '.pkl'	# TODO

	# stdscr = curses.initscr()  # initialise it
	# stdscr.clear()  # Clear the screen

	if args.default_name :
		print os_def_name
		sys.exit(0)



	if args.debug :
		__log.setLevel( log.DEBUG )

	elif args.verbose == 0 :
		__log.setLevel( log.WARNING )

	elif args.verbose == 1 :
		__log.setLevel( log.ERROR )

	elif args.verbose == 2 :
		__log.setLevel( log.INFO )


	__log.info(header)
	if args.debug :
		__log.debug("Debugging mode")
	else :
		__log.warning("Verbosity set to: %d" % args.verbose)

	__log.warning('')


	if args.diff != None :
		image1 = io.loadImage( args.diff[0] )
		image2 = io.loadImage( args.diff[1] )
		differ.diffSystem( image1, image2 )
		__log.warning( "\n" )
		sys.exit()


	if args.image :
		outfile = args.image
		fs = maker.create_Image(os_def_name)
		io.saveImage(outfile, fs)