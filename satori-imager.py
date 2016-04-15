#!/usr/bin/python
#-*- coding: utf-8 -*-

import platform as plat

import logging as log
import argparse

import lib.image_maker as maker
import lib.image_io as io
import lib.definitions as defs

import lib.helpers.signal_handler

import signal
import sys

header = defs.header.format( "OS filesystem image Creator" )

log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )

# import lib.helpers.custom_log_format as cLog
# handler = log.StreamHandler()
# handler.setFormatter(cLog.CustomFormatter)
# __log.addHandler(handler)
#setFormatter(cLog.CustomFormatter)



if __name__ == "__main__" :

	os_def_name = plat.platform()

	parser = argparse.ArgumentParser( description = 'Crawls the whole filesystem and creates an image of it to a file.' )

	parser.add_argument( 'image', help = 'Set image filename. Default filename for this system is "%s.*"' % os_def_name, \
									default = os_def_name, nargs = '?' )

	parser.add_argument( '--type', '-t', help = 'Choose the file type of the images',\
										type = str, choices = ['pickle', 'json', 'sqlite'], default = 'json' )

	parser.add_argument( '--no-gzip', '-ng', help = 'Image IO will *NOT* use gzip (larger but readable files)',\
							 action = 'store_true', default = False )

	verb = parser.add_mutually_exclusive_group()
	verb.add_argument( '--verbose', '-v' , help = 'verbose mode', action = 'count', default = 0 )
	verb.add_argument( '--debug' , '-d', help = 'debugging mode', action = 'store_true', default = False )
	verb.add_argument( '--quiet', '-q' , help = 'quiet mode', action = 'store_true', default = False )

	deepness = parser.add_mutually_exclusive_group()
	deepness.add_argument( '--filetypes', help = "Try to guess filetypes with mimes and 'file' command (slower)",\
							 action = 'store_true', default = False )
	deepness.add_argument( '--text', help = "Guess file types and save all text contents of a file in the image (very slow! Useful for config files)",\
							action = 'store_true', default = False )

	parser.add_argument( '--hash', help = "Calculate and store the SHA-256 of every file in the image (slower)",\
							action = 'store_true', default = False )

	parser.add_argument( '--threads', help = 'Use threads to create the Filesystem Image (good for multiple IO calls)',\
							 type = int, default = 4 )


	parser.add_argument( '--exclude', '-x', help = 'Select directories to be Excluded', nargs = '+', type = str, default = [] )
	parser.add_argument( '--include', '-i', help = 'Select directories to be Included', nargs = '+', type = str, default = [] )
	parser.add_argument( '--clear-excluded', '-c', help = 'Clear default excluded directories', action = 'store_true', default = False)
	parser.add_argument( '--show-excluded', help = 'Show excluded directories and exit', action = 'store_true', default = False)

	args = parser.parse_args()


	filename = args.image

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


	'''	================================================ DEEPNESS OPTION ================================================ '''

	if args.filetypes :
		maker.__modes.append( 'type' )
		filename += '_TYPE'

	elif args.text :
		maker.__modes.append( 'type' )
		maker.__modes.append( 'text' )
		filename += '_TYPE_TEXT'

	if args.hash :
		maker.__modes.append( 'hash' )
		filename += '_HASH'




	'''	================================================ COMPRESSION OPTION ================================================ '''

	if args.no_gzip :
		__log.info( "* Compression is Disabled! *" )

	else :
		__log.info( "Compression is Enabled!" )
		io.__use_gzip = True
		exten += '.gz'


	if args.threads < 1 or args.threads > 64 :
		__log.info( "* Thread number incorrect! Using single-threading. *" )
		args.threads = 1
	# else :
		# __log.info( "* Using %d Threads *" % args.threads )

	maker.__threads = args.threads


	outfile = (filename + exten).replace(' ','_')

	__log.info('File "%s" will be created' % outfile)
	__log.info('')



	'''	================================================ INCLUDE/EXCLUDE OPTION ================================================ '''

	excludes = set(args.exclude)
	includes = set(args.include)


	double_types = excludes & includes
	if len(double_types) != 0 :
		__log.critical( 'Those directories where both "included" and "excluded" :')
		for dirs in double_types :
			__log.critical( '-> %s' % dirs )
		__log.critical('Exiting...')
		sys.exit(2)

	if args.clear_excluded :
		maker.__excludes = set()

	maker.__excludes = maker.__excludes | excludes
	maker.__excludes = maker.__excludes - includes



	if args.show_excluded :
		if len(maker.__excludes) == 0 :
			__log.critical('All directories are included!')
		else :
			__log.critical( 'Excluded Directories :' )
			for excl in maker.__excludes :
				__log.critical( '-> %s' % excl )

		__log.error( "Directories/Files ALWAYS excluded (error prone) :" )
		for excl in maker.hard_excludes :
			__log.error( '-> %s' % excl )
		sys.exit(0)



	fs = maker.create_Image( os_def_name )
	__log.warning( 'Image generated! Creating File...' )
	io.saveImage( outfile, fs, args.type )