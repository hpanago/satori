#!/usr/bin/python
#-*- coding: utf-8 -*-

import platform as plat

import logging as log
import argparse

import lib.image_maker as maker
import lib.image_io as io
import lib.definitions as defs


header = '''
Welcome to {0} Imager
OS filesystem image Creator
Version {1}
'''.format(defs.program_name, defs.version)


log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



if __name__ == "__main__" :

	os_def_name = plat.platform()

	parser = argparse.ArgumentParser( description = 'Crawls the whole filesystem and creates an image of it to a file.' )

	parser.add_argument( 'image', help = 'Set image filename. Default filename for this system is "%s.*"' % os_def_name, \
									default = os_def_name, nargs = '?' )

	parser.add_argument( '--type', '-t', help = 'Choose the file type of the images',\
										type = str, choices = ['pickle', 'json', 'sqlite'], default = 'json')

	parser.add_argument( '--no-gzip', '-ng', help = 'Image IO will *NOT* use gzip (larger but readable files)', action = 'store_true', default = False)

	verb = parser.add_mutually_exclusive_group()
	verb.add_argument( '-v', '--verbose' , help = 'verbose mode', action = 'count', default = 0 )
	verb.add_argument( '--debug' , '-d', help = 'debugging mode', action = 'store_true', default = False )
	verb.add_argument( '--quiet', '-q' , help = 'quiet mode', action = 'store_true', default = False )


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

	__log.warning(header)
	if args.debug :
		__log.debug("* Debugging mode *")
	else :
		__log.warning("Verbosity set to: %d" % args.verbose)


	'''	================================================ FILE TYPE OPTION ================================================ '''

	if args.type == 'json' :
		exten = '.jsn'

	elif args.type == 'pickle' :
		exten = '.pkl'

	elif args.type == 'sqlite' :	# TODO
		exten = '.db'


	'''	================================================ COMPRESSION OPTION ================================================ '''

	if args.no_gzip :
		__log.info( "* Compression is Disabled! *" )
	else :
		__log.info( "Compression is Enabled!" )
		io.__use_gzip = True
		exten += '.gz'

	outfile = (args.image + exten).replace(' ','_')

	__log.info('File "%s" will be created' % outfile)
	__log.info('')

	fs = maker.create_Image( os_def_name )
	io.saveImage( outfile, fs, args.type )