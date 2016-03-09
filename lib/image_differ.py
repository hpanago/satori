import cPickle as pickle
import json
import os
import logging as __logger

tags = [ 'content', 'path', 'filename', 'type', 'size', 'privileges', 'owner', 'group', 'SHA2' ]
criticals = tags[5 : 7]


__NA = 'N/A'
__non_exist = 'non-existent'
__not_original = 'not-original'

# __logger = logging.getLogger( __name__ )
__logger.basicConfig(format = '\t+ %(message)s')

__file_tmpl = "File '{0}'"

templates = {}
templates[__non_exist] 		= "%s exists in the original but not in the given image!" % __file_tmpl
templates[__not_original]	= "%s is not existent in the original image."	% __file_tmpl
templates['type']			= "%s has different type. Original is {1} and given is {2} !" % __file_tmpl
templates['size']			= "%s size differes. Original is of size {1} bytes and given is {2} !" % __file_tmpl
templates['privileges']		= "%s has different privileges! Originals are {1} and given are {2} !" % __file_tmpl
templates['owner']			= "%s has different owner! Original owner is {1} and the file is owned by {2} !" % __file_tmpl
templates['group']			= "%s has different group! Original group is {1} and the file's group is {2} !" % __file_tmpl
templates['SHA2']			= "%s has different hash. Original file's hash is '{1}' and the file's hash is '{2}' !" % __file_tmpl


def reportDiff(entry, diff_type, f1 = '', f2 = '') :
	'''		Reports the difference depending on its type	'''

	full_path = ( entry['path'] + os.sep + entry['filename'] )
	# .replace('//','/')


	if diff_type == __not_original :
		__logger.info( templates[ __non_exist ].format( full_path ) )
		return

	elif diff_type == __non_exist :
		__logger.warning( templates[ __not_original ].format( full_path ) )
		return

	if diff_type in criticals :
		__logger.critical( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )
	else :
		__logger.warning( templates[ diff_type ].format( full_path, f1[diff_type], f2[diff_type] ) )


	# print entry['path'] + "  " + entry['filename'] + " " + diff_type
	# print '--'
#	print "Entry '{0}' exists at {1} while doesn't at {2}".format( entry, exists['filename'], nexists['filename'] )



def diffFile(file1, file2) :

	# print file1['path'] + "  " + file1['filename']

	for tag in tags[1:-1] :	# exclude content
		if file1[tag] == __NA :
			continue
		if file1[tag] != file2[tag] :
			reportDiff (file2, tag, file1, file2)
			return 1

	if file1['type'] == 'directory' :

		diffFolder( file1['content'], file2['content'] )
#	for file in contents


def diffFolder(folder1, folder2) :

	loc1 = set( folder1.keys() )
	loc2 = set( folder2.keys() )


	diffs = loc1 - loc2

	for diff in diffs :
		reportDiff (diff, __non_exist, folder1, folder2)


	diffs = loc2 - loc1

	for diff in diffs :
		reportDiff (diff, __not_original, folder2, folder1)


	for key in (loc1 & loc2) :
		diffFile( folder1[key], folder2[key] )
	pass


def diffSystem(sys1, sys2) :

	diffFile(sys1, sys2)



if __name__ == '__main__' :
	import sys
	f1 = open( sys.argv[1], 'r' )
	f2 = open( sys.argv[2], 'r' )
	
	sys1 = pickle.load(f1)
	sys2 = pickle.load(f2)
	
	diffSystem(sys1, sys2)