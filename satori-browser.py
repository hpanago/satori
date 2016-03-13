#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse
import lib.image_io as io
import logging as log

import lib.definitions as defs


header = '''
Welcome to {0} Differ
OS filesystem image Browser
Version {1}
'''.format(defs.program_name, defs.version)


log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



if __name__ == "__main__" :

	parser = argparse.ArgumentParser( description = 'Browses inside a {0} image'.format( defs.program_name ) )

	parser.add_argument( 'image', help = "Satori image to open", type = str )

	parser.add_argument( '--type', '-t', help = 'Choose the file type of the image',\
										type = str, choices = ['pickle', 'json', 'sqlite'], default = 'json')

	parser.add_argument( '--no-gzip', '-ng', help = 'Image IO will *NOT* use gzip', action = 'store_true', default = False)


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

	print 'Ready!'


	while True :
		inp = raw_input ( '%s $ ' % 'satori' )
		if inp == 'exit' :
			break