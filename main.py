#!/usr/bin/python

import sys
import os
import platform as plat

import logging as log
import argparse

import lib.image_maker as maker
import lib.image_differ as differ
import lib.image_io as io


if __name__ == "__main__" :
	os_def_name = plat.platform()
	parser = argparse.ArgumentParser( prog = sys.argv[0], description = 'Diffs files of a live OS with the ones of its fresh installation' )
	utility = parser.add_mutually_exclusive_group()
	utility.add_argument( '--image', help = 'Create an image file named as "IMAGE"', type = str, default = '{0}.pkl'.format(os_def_name), nargs = '?' )
	utility.add_argument( '--diff', help = 'Diff two filesystem images', nargs = 2, type = str, metavar = 'IMAGE' )
	parser.add_argument( '--default-name', '-d', help = 'Just print the default filename for this machine and exit', action = 'store_true' )
	parser.add_argument( '-v', '--verbose' , help = 'verbose mode', action = 'store_true', default = False )


	args = parser.parse_args()

	exten = '.pkl'

	if args.default_name :
		print os_def_name
		sys.exit(0)

	if args.verbose :
		log.basicConfig( level = log.INFO )
	else :
		log.basicConfig( level = log.WARNING )
	log.basicConfig(format = "%(message)s")

	print args.diff
	sys.exit()
	# try : 
	if args.image == None:
		args.image = os_def_name + exten

	if args.image :
		outfile = args.image
		fs = maker.crawl_filesystem()
		io.saveImage(outfile, fs)