#-*- coding: utf-8 -*-
import os
import sys
import difflib
import re
# from difflib_data import *
import logging as log

from lib.definitions import meta_templates, meta_tags
# from lib.definitions import file_tags as tags

tags = [ 'content', 'path', 'filename', 'type', 'size', 'privileges', 'owner', 'group', 'SHA2' ]
criticals = tags[5 : 7]


__NA = 'N/A'
__non_exist = 'non-existent'
__not_original = 'not-original'

__logger = log.getLogger( '__main__' )
#__logger.basicConfig(format = '\t+ %(message)s')

__file_tmpl = "File '{0}'"

templates = {}
templates[__non_exist] 		= "[EXISTENCE] %s exists in the original but not in the given image!" % __file_tmpl
templates[__not_original]	= "[EXISTENCE] %s is not existent in the original image."	% __file_tmpl
templates['content']		= "[ALTERATION] %s has different contents !" % __file_tmpl
templates['type']			= "[ALTERATION] %s has different type. Original is {1} and given is {2} !" % __file_tmpl
templates['size']			= "[ALTERATION] %s size differs. Original is of size {1} bytes and given is {2} !" % __file_tmpl
templates['privileges']		= "[CHMOD-ED] %s has different privileges! Originals are {1} and given are {2} !" % __file_tmpl
templates['owner']			= "[CHOWN-ED] %s has different owner! Original owner is {1} and the file is owned by {2} !" % __file_tmpl
templates['group']			= "[CHOWN-ED] %s has different group! Original group is {1} and the file's group is {2} !" % __file_tmpl
templates['SHA2']			= "[ALTERATION] %s has different hash. Original file's hash is '{1}' and the file's hash is '{2}' !" % __file_tmpl

meta_templates['original'] = "Original System Image:"
meta_templates['subject'] = "Subject System Image:"



def reportMeta(meta, original = False) :

	__logger.info( '==================================================' )
	if original :
		__logger.info( meta_templates['original'] )
	else :
		__logger.info( meta_templates['subject'] )

	for tag in meta_tags :
		if tag == 'program' :
			continue
		__logger.info( meta_templates[ tag ].format( meta[ tag ] ) )
	
	__logger.info( '==================================================' )



def reportDiff(entry, diff_type, f1 = '', f2 = '') :
	'''		Reports the difference depending on its type	'''
	__logger.debug( 'reportDiff( %s, %s, f1, f2 )' % (entry, diff_type) )


	full_path = ( entry )

	if diff_type == __not_original :
		__logger.info( templates[ __not_original ].format( full_path ) )
		return

	elif diff_type == __non_exist :
		__logger.warning( templates[ __non_exist ].format( full_path ) )
		return

	if diff_type in criticals :
		__logger.critical( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )
	else :
		__logger.warning( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )



	# if diff_type == tags[0] :	# content
	# 	__logger.warning( templates['content'].format( full_path ) )
	if 'text' in f1['type'] :
		differ = difflib.Differ()
		f1_lines = f1['content'].decode('base64').splitlines()
		f2_lines = f2['content'].decode('base64').splitlines()
		diff = differ.compare( f1_lines, f2_lines )
		__logger.info( '\n'.join( diff ) )
		# try:
		# 	while 1:
		# 		__logger.info( diff.next() )
		# except:
		# 	pass



def diffFile(file1, file2) :

	# __logger.debug( 'diffFile( %s, %s )' % ( file1['filename'], file2['filename'] ) )

	full_path = file1['path'] + os.sep + file1['filename']

	for tag in tags[:] :	# exclude content
		__logger.debug( 'Checking files %s in %s' % ( file1['filename'], file1['path'] ) )
		if file1[tag] == __NA or file2[tag] == __NA :	# make it better by checking both type groups

			continue
		if file1[tag] != file2[tag] :
			reportDiff (full_path, tag, file1, file2)

	if file1['type'] == 'directory' :

		diffFolder( file1, file2 )



def diffFolder(folder1, folder2) :

	loc1 = set( folder1['content'].keys() )
	loc2 = set( folder2['content'].keys() )

	base_path = folder1['path'] + os.sep + folder1['filename'] + os.sep

	diffs = loc1 - loc2

	for diff in diffs :
		full_path = base_path + diff
		reportDiff (full_path, __non_exist, folder1, folder2)

	diffs = loc2 - loc1

	for diff in diffs :
		full_path = base_path + diff
		reportDiff (full_path, __not_original, folder2, folder1)


	for key in (loc1 & loc2) :
		diffFile( folder1['content'][key], folder2['content'][key] )



def diffSystem(sys1, sys2, root_dir) :

	meta1 = sys1['meta']
	meta2 = sys2['meta']
	reportMeta( meta1, True )
	reportMeta( meta2, False )

	__logger.info( '\n' )


	root_pathlist = re.split( '\/+', root_dir )

	sys1 = sys1['system']
	sys2 = sys2['system']

	for dir_ in root_pathlist :

		if not dir_ :
			continue

		try :
			sys1 = sys1['content'][ dir_ ]
		except :
			__logger.critical( "Directory '%s' does not exist in Original Image" % os.sep.join(root_pathlist) )
			sys.exit(1)
		try :
			sys2 = sys2['content'][ dir_ ]
		except :
			__logger.critical( "Directory '%s' does not exist in Given Image" % os.sep.join(root_pathlist) )
			sys.exit(1)

		# sys2 = sys2['content'][ dir_ ]


	diffFile(sys1, sys2)

