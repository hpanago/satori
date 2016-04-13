#-*- coding: utf-8 -*-
import sys
import json
import mimetypes
import hashlib
from stat import *
import os
import socket
from datetime import date

# import multiprocessing as mproc
import threading as thrd
# from multiprocessing.pool import ThreadPool
from Queue import Queue
from time import sleep

import logging as log

import definitions as defs

import helpers.signal_handler



excludes = set()
excludes.add('/proc')
excludes.add('/run')
excludes.add('/sys')
excludes.add('/dev')
excludes.add('/boot')
excludes.add('/media')
excludes.add('/usr/src')
excludes.add('/var/log')


excludes.add('/root')
excludes.add('/home')


__logger = log.getLogger( '__main__' )

__NA = 'N/A'

creator_tags = ['program', 'version', 'system']

creator_template = {}
creator_template['program'] = 'The image is made by {0}.'
creator_template['version'] = 'Version: {0}'
creator_template['system'] = 'Found system: {0}'

__modes = []

__threads = 1

__crawling_done = False
queue = Queue()


def thread_worker( id ) :

	while not __crawling_done :
		# task = queue.get(True, 0.05)
		try :
			task = queue.get(True, 0.05)
			# task = queue.get_nowait(True, 0.05)
		except :
			# try :
			# 	sleep(0.1)
			# except :
				# continue				
			continue
		full_path, name, ret, folder = task

		key = full_path + os.sep + name 

		crawl_folder( full_path, name, ret )

		folder[ 'content' ] = ret

		queue.task_done()


def get_root_dir() :
	""" http://stackoverflow.com/questions/12041525/a-system-independent-way-using-python-to-get-the-root-directory-drive-on-which-p """

	dr = os.path.splitdrive( sys.executable )
	if not dr[0] :		#	dr[0] is empty, we have *nix system, root dir is '/' handled later
		return '/'
	else :				#	dr[0] is like 'C:\\', we have a Windows system
		return dr[0]

		'''		This one returns the base location of the script	'''
    # return os.path.abspath(os.sep)



def hashfile(afile, hasher, blocksize = 65536):
	'''
http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
	'''
	if afile == None :
		return ''
	buf = afile.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	afile.close()
	hash_str = hasher.hexdigest()
	__logger.debug( "hash: '%s' " % hash_str )
	return 



def create_file_obj(full_path, name, fobj) :

	full_name = os.path.join(full_path, name)
	# __logger.debug( 'create_file_obj( %s )' % full_name )

	if 'type' in __modes :
		mime = os.popen( "file '{0}' ".format( full_name ) ).read().split( ':' )[-1].strip()	# main.py: Python script, ASCII text executable		# sample output
	else :
		mime = mimetypes.guess_type( full_name )[0]
		if mime == None :
			mime = __NA

	stat_obj = os.lstat(full_name)	# lstat instead of stat to NOT follow symlinks

	fobj['filename'] = name
	fobj['path'] = full_path
	fobj['owner'] = stat_obj[ST_UID]
	fobj['group'] = stat_obj[ST_GID]
	fobj['size'] = stat_obj[ST_SIZE]
	fobj['privileges'] = str( oct( stat_obj[ST_MODE] ) )
	fobj['type'] = mime
	fobj['SHA2'] = __NA

	if full_name in excludes :
		return fobj

	if S_ISLNK(stat_obj.st_mode) :
		return fobj

	if os.path.isdir(full_name) :
		fobj['type'] = 'directory'
		ret = dict()
		# fobj['content'] = dict()
		args = (full_path, name, ret, fobj)
		queue.put(args)

	elif 'text' in mime and 'text' in __modes:
		try :
			f = open( full_name, 'r' )
			fobj['content'] = f.read().strip()
			f.close()
		except Exception as e :
			__logger.debug( "'%s' while opening file '%s' for text reading!" % (str(e),full_name) )
			pass

	else :
		fobj['content'] = __NA

		if 'hash' in __modes :
			try :
				f = open( full_name, 'rb' )
				fobj['SHA2'] = hashfile(f, hashlib.md5())
				# fobj['SHA2'] = hashfile(f, hashlib.sha256())
				f.close()

			except Exception as e :
				__logger.debug( "'%s' while opening file '%s' for hashing!" % (str(e),full_name) )
				pass

	return fobj



def crawl_folder(base, folder_path, fset) :

	full_path = os.path.join( base, folder_path )

	try : 

		for file in os.listdir(full_path) :

			key = full_path + os.sep + file 
			ret = dict()

			create_file_obj(full_path, file, ret)
			# fset[ key ] = ret
			fset[ file ] = ret

	except OSError :
			__logger.info( "\t[*]	Listing folder '{0}' failed!".format( full_path ) )

	return fset






def crawl_filesystem() :

	threads = []
	for i in range(__threads) :
		t = thrd.Thread( target = thread_worker, args = (i,) )
		threads.append( t )
		t.setDaemon( True )
		t.start()

	root = get_root_dir()
	ret = dict()
	create_file_obj('', root, ret)

	__crawling_done = True
	queue.join()


	return ret



def create_Image(system_name = 'unknown') :

	fsys = {}

	fsys['meta'] = {}
	fsys['meta']['program'] = defs.program_name
	fsys['meta']['version'] = defs.version	
	fsys['meta']['system'] = system_name
	fsys['meta']['date'] = str(date.today())
	fsys['meta']['excludes'] = list(excludes)
	fsys['meta']['modes'] = __modes
	fsys['meta']['user'] = os.popen('whoami').read().strip()
	fsys['meta']['UID'] = os.popen('id -u').read().strip()
	fsys['meta']['GID'] = os.popen('id -g').read().strip()
	fsys['meta']['hostname'] = socket.gethostname().strip()

	__logger.info( creator_template['system'].format( fsys['meta']['system'] ) )
	__logger.info( "Excluded directories:" )
	for dir in excludes :
		__logger.info( "-> "+dir )

	fsys['system'] = crawl_filesystem()

	return fsys



if __name__ == "__main__" :		# TODO standalone module

	import platform
	fsys = crawl_filesystem(platform.platform())
	import gzip
	f = gzip.open ('file_system.jsn.gz', 'wb')
	f.write( json.dumps( fsys ) )
	f.close()
