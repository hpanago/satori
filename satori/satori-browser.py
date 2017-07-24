#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import lib.image_io as io
import logging as log

import sys

import lib.definitions as defs
from lib.image_browser import *

import lib.helpers.signal_handler

header = defs.header.format( "OS filesystem image Browser" )


log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



if __name__ == "__main__" :

	parser = argparse.ArgumentParser( description = 'Browses inside a {0} image'.format( defs.program_name ) )

	parser.add_argument( 'image', help = "Satori image to open", type = str )

	parser.add_argument( '--type', '-t', help = 'Choose the file type of the image',\
										type = str, choices = ['pickle', 'json', 'sqlite'], default = 'json')

	parser.add_argument( '--no-gzip', '-ng', help = 'Image IO will *NOT* use gzip', action = 'store_true', default = False)

	parser.add_argument( '--info', '-i', help = "Display the Image's info and exit",\
										action = 'store_true', default = False)


	args = parser.parse_args()



	'''	================================================ HEADER + INFO ================================================ '''

	__log.warning(header)


	'''	================================================ COMPRESSION OPTION ================================================ '''

	if args.no_gzip :
		__log.info( "* Compression is Disabled! *" )
	else :
		__log.info( "Compression is Enabled!" )
		io.__use_gzip = True

	print 'Loading Image...'
	image = io.loadImage( args.image, args.type )
	print

	if args.info :
		print get_info_string( image )
		sys.exit(0)

	satori_shell = SatoriShell(image)
	satori_shell.cmdloop(  )
