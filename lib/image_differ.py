#-*- coding: utf-8 -*-
import os
import sys
import difflib
import re
# from difflib_data import *
import logging as log

from lib.definitions import meta_templates, meta_tags
# from lib.definitions import file_tags as tags

from tree import Node as DiffNode
from termcolor import colored 

tags = [ 'content', 'path', 'filename', 'type', 'size', 'privileges', 'owner', 'group', 'SHA2' ]

criticals = [ 'privileges', 'owner', 'group' ]
content_alterations = ['content', 'size', 'SHA2']
metadata_alterations = ['owner', 'group', 'privileges', 'type']


DIFF_TREE = None
CUR_NODE = None

__NA = 'N/A'
__non_exist = 'non-existent'
__not_original = 'not-original'

__logger = log.getLogger( __name__ )

log.basicConfig(format = '%(message)s', stream = sys.stdout)
__logger.setLevel( log.INFO )

__file_tmpl = "File '{0}'"
__dir_tmpl = "Directory '{0}'"

templates = {}
templates[__non_exist] 		= u"[EXISTENCE] %s exists in the original but not in the given image!" % __file_tmpl
templates[__not_original]	= u"[EXISTENCE] %s is not existent in the original image."	% __file_tmpl
templates['content']		= u"[ALTERATION] %s has different contents !" % __dir_tmpl
templates['type']			= u"[ALTERATION] %s has different type. Original is {1} and given is {2} !" % __file_tmpl
templates['size']			= u"[ALTERATION] %s size differs. Original is of size {1} bytes and given is {2} !" % __file_tmpl
templates['privileges']		= u"[CHMOD-ED] %s has different privileges! Originals are {1} and given are {2} !" % __file_tmpl
templates['owner']			= u"[CHOWN-ED] %s has different owner! Original owner is {1} and the file is owned by {2} !" % __file_tmpl
templates['group']			= u"[CHOWN-ED] %s has different group! Original group is {1} and the file's group is {2} !" % __file_tmpl
templates['SHA2']			= u"[ALTERATION] %s has different hash !" % __file_tmpl
# templates['SHA2']			= u"[ALTERATION] %s has different hash. Original file's hash is '{1}' and the file's hash is '{2}' !" % __file_tmpl

meta_templates['original'] = "Original System Image:"
meta_templates['subject'] = "Subject System Image:"




def reportMeta(meta, original = False) :

	__logger = log.getLogger( '__main__' )
	# ch = log.StreamHandler(sys.stderr)
	# __logger = log.setHandler( ch )

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


def __getLogMethod( diff_type ) :

	if diff_type == __not_original :
		log = __logger.info

	elif diff_type == __non_exist :
		log = __logger.warning

	elif diff_type in criticals :
		log = __logger.critical

	else :
		log = __logger.warning

	return log


def contentDiff( f1, f2 ) :
	if 'text' in enabledModes :
		differ = difflib.Differ()
		f1_lines = f1['content'].decode('base64').splitlines()
		f2_lines = f2['content'].decode('base64').splitlines()
		diff = differ.compare( f1_lines, f2_lines )
		__logger.info( '\n'.join( diff ) )


def reportDiff( entry, diff_list, f1 = '', f2 = '' ) :
	'''		Reports the difference depending on its type	'''
	__logger.debug( '	reportDiff( %s, %s, f1, f2 )' % (entry, diff_list) )

	full_path = ( entry )
	entry = entry.split( os.sep )[-1]

	node = None

	diff_list_str = ', '.join(diff_list)
	# diff_list_str = colored( diff_list_str, attrs=['underline',] )
	diff_list_str = '  -- [%s]' % diff_list_str
	# diff_list_str = colored( ' - [','white' ) + '%s] ' % diff_list_str

	for diff_type in diff_list :

		__logger.debug( "Now Reporting diff on '%s'" % diff_type )

		log = __getLogMethod( diff_type )
		if diff_type == __not_original :

			node = DiffNode( colored( entry, 'green' ) )

			log( templates[ diff_type ].format( full_path ) )
			continue
			# return

		elif diff_type == __non_exist :

			node = DiffNode( colored( entry, 'red' ) )

			log( templates[ diff_type ].format( full_path ) )
			continue
			# return



		if diff_type in metadata_alterations :		
			node = DiffNode( colored( entry + diff_list_str, 'white', 'on_yellow', attrs=['bold',] ) )
			log( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )



		if diff_type in content_alterations :
			node = DiffNode( colored( entry + diff_list_str, 'yellow' ) )
			log( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )

			if diff_type == 'content' :
				contentDiff ( f1, f2 )
			# break

	global CUR_NODE
	if node :
		CUR_NODE.add_child(node)



def diffFile(file1, file2) :

	# __logger.debug( 'diffFile( %s, %s )' % ( file1['filename'], file2['filename'] ) )

	full_path = file1['path'] + os.sep + file1['filename']
	diff_list = []

	for tag in tags[1:] :	# exclude content
		__logger.debug( "Checking files %s in %s for diff on '%s'" % ( file1['filename'], file1['path'], tag ) )

		if file1[tag] == __NA or file2[tag] == __NA :	# make it better by checking both type groups
			continue

		if file1[tag] != file2[tag] :
			diff_list.append(tag)

	if file1['type'] == 'directory' :
		diffFolder( file1, file2 )

	reportDiff (full_path, diff_list, file1, file2)



def diffFolder( folder1, folder2 ) :

	loc1 = set( folder1['content'].keys() )
	loc2 = set( folder2['content'].keys() )

	base_path = folder1['path'] + os.sep + folder1['filename'] + os.sep

	diffs = loc1 - loc2

	global CUR_NODE
	global DIFF_TREE

	prev_node = CUR_NODE
	node = DiffNode( base_path )

	CUR_NODE.add_child( node )
	CUR_NODE = node

	for diff in diffs :
		full_path = base_path + diff
		reportDiff (full_path, [ __non_exist, ] , folder1, folder2)

	diffs = loc2 - loc1

	for diff in diffs :
		full_path = base_path + diff
		reportDiff (full_path, [ __not_original, ], folder2, folder1)


	for key in (loc1 & loc2) :
		diffFile( folder1['content'][key], folder2['content'][key] )

	temp_node = CUR_NODE
	CUR_NODE = prev_node

	if temp_node.is_leaf() :
		CUR_NODE.delete_child( temp_node )



def __init_diff_tags() :

	if 'type' not in enabledModes :
		metadata_alterations.remove('type')

	if 'hash' not in enabledModes :
		content_alterations.remove('SHA2')



def diffSystem(sys1, sys2, root_dir) :

	meta1 = sys1['meta']
	meta2 = sys2['meta']
	reportMeta( meta1, True )
	reportMeta( meta2, False )

	__logger.info( '\n' )

	global enabledModes 
	enabledModes = meta1['modes'] and meta2['modes']	# 
	__init_diff_tags()


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


	global CUR_NODE
	global DIFF_TREE

	DIFF_TREE = DiffNode( "	"+"="*20+"	Diff Tree	"+"="*20 )

	CUR_NODE = DIFF_TREE

	diffFile(sys1, sys2)

	print >> sys.stderr, DIFF_TREE