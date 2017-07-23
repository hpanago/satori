#-*- coding: utf-8 -*-

import cmd
import re
import os
from pprint import pprint 

from lib.definitions import meta_templates, meta_tags

color = {}
color['gray'] = '\033[04;39m'
color['green'] = '\033[01;32m'
color['red'] = '\033[01;31m'
color['blue'] = '\033[01;34m'
color['END'] = '\033[00m'


class SatoriShell (cmd.Cmd) :

	# commands = [ 'cd', 'ls', 'stat', 'cat', 'file', 'hash', 'pwd', 'info' ]
	debugs = [ 'keys', 'value' ]

	prompt_format = color['gray'] + "{{Satori}}" + color['END'] + ' %s%s@%s%s ' + color['blue'] + '{0} %s '+color['END']		# "{Satori} john@Lucinda / $ "
	prompt = prompt_format.format('/')

	dir_regex = '(\.\./?)+'

	cd_stack = []


	def change_prompt(self, dir) :

		path = dir['path'] + os.sep + dir['filename']
		if path.startswith(os.sep*2) :
			path = path[1:]

		self.prompt = self.prompt_format.format(path)



	def __init__ (self, image) :
		cmd.Cmd.__init__(self)
		self.__image = image
		self.__wd = image['system']
		self.__base = self.__wd
		self.__user = image['meta']['user']
		self.__host = image['meta']['hostname']

		col = color['green']
		symb = '$'
		if self.__image['meta']['UID'] == 0 :
			col = color['red']
			symb = '#'

		self.prompt_format = self.prompt_format % (col, self.__user, self.__host, color['END'], symb)
		self.change_prompt(self.__wd)



	def exists (self, name) :
		if ( name in self.__wd['content'].keys() ) :
			return True
		else :
			print "	File '%s' doesn't exist in current directory!" % name
			return False


	def do_cat (self, line) :
		"""	Typical UNIX command. Catenates the contents of text file"""
		if "text" not in self.__image['meta']['modes'] :
			print "Image file does not support 'cat'. File contents are not saved."
			return

		arg = line.split()
		begin = "-----BEGIN '{0}'-----"
		ending = "-----END   '{0}'-----"
		for a in arg :
			if self.exists( a ) :
				if "text" in self.__wd['content'][a]['type'] :
					print begin.format(a)
					print self.__wd['content'][a]['content'].decode('base64')
					print ending.format(a)
				else :
					print "'%s': Unsupported command for file type '%s'" % (a, self.__wd['content'][a]['type'])


	def do_file (self, line) :
		"""	Typical UNIX command. Catenates the contents of text file"""
		arg = line.split()
		for a in arg :
			if self.exists( a ) :
				print "%s: %s" % ( a, self.__wd['content'][a]['type'] )


	def do_id (self, line) :
		"""	Typical UNIX command. Added for extra flavour"""
		print "	uid=%s(%s)	gid=%s"	% (self.__image['meta']['UID'], self.__image['meta']['user'], self.__image['meta']['GID'] )

	def do_info (self, line) :
		"""	Prints out Information about the Satori Image being browsed."""
		print
		print get_info_string( self.__image )
		print


	def do_ls (self, line) :
		"""	Typical UNIX command. Lists directories."""
		# if line.strip() : 

		target = self.__wd
		arg = line.split()

		if '-l' in arg :
			_l = True
			arg.remove('-l')
		else :
			_l = False

		if len(arg) > 0 :

			if self.exists (arg[0]) :
				target = self.__wd['content'][arg[0]]
			else :
				return


		if target['type'] == 'directory' :
			files = target['content'].keys()
			if not _l :
				print "	".join( files )

			else :
				print "	{0:20}  |  {1:>10}	{2:>11}	{3:8}	{4:8}	{5:8}".format\
				( "Filename", "Size", "Privileges", "User", "Group", "Filetype" )
				print "	{0:20}  |  {1:10}	{2:11}	{3:8}	{4:8}	{5:8}".format\
				( "=" * 20,"=" * 10,"=" * 11,"=" * 8,"=" * 8, "=" * 8) 

				for k in files :
					f = target['content'][k]
					print "	{0:20}  |  {1:10}	{2:>11}	{3:<8}	{4:<8}	{5:8}".format\
							 ( f['filename'], f['size'], f['privileges'], f['owner'], f['group'], f['type'] )

		else :
			print "	'%s' is not a directory" % target['filename'] 
		return




	def complete_ls (self, text, line, begidx, endidx) :
		return self.complete_cd ( text, line, begidx, endidx ) 


	def do_cd (self, line) :

		f = line.strip().split()
		if not f :
			return
		target = f[0]
		dirs = re.split('\/+', target)
		#maybe this print statement and..
		print dirs

		wd = self.__wd
		for d in dirs :
			if not d :
				continue 

			if d == '.' :
				continue
			
			if d == '..' :
				try :
					wd = self.cd_stack.pop()
				except :
					pass
				continue

			if self.exists( d ) and wd['content'][d]['type'] == 'directory' :
				self.cd_stack.append(wd)
				wd = wd['content'][d]
				#this one, could be removed, for a more bash-like shell?
				print d

		self.__wd = wd
		self.change_prompt(self.__wd)
 		return


	def complete_cd (self, text, line, begidx, endidx) :
		if not text :
			return self.__wd['content'].keys()
		else :
			return [ f for f in self.__wd['content'].keys() if f.startswith(text) ]

	def complete_cat (self, text, line, begidx, endidx) :
		return self.complete_cd ( text, line, begidx, endidx ) 


	def do_stat (self, line) :
		"""	Typical UNIX command. Displays collected information about files."""
		f = line.strip()

		if not f :
			target = self.__wd

		else :
			if self.exists(f) :
				target = self.__wd['content'][f]
			else :
				return

		for k in target.keys() :
			if k != 'content' :
				print  "	%s : %s" % ( k, target[k] ) 


	def do__keys (self, line) :
		# """Debugging command. Shows the "working directory's" dictionary keys"""
		for k in self.__wd.keys() :
			print "	%s" % k


	def do__value (self, line) :
		# """Debugging command. Shows the "working directory's" dictionary keys"""
		key = line.strip()
		if self.__wd[ 'type' ] == 'directory' and key == 'content' :
			self.do_ls('')
			return
		try :
			ret = self.__wd[key]
			print "	%s" % ret
		except :
			print "No such key..."


	def do__trace_cd (self, line) :
		# """Debugging command. Shows the "cd stack-trace" """
		print [x['filename'] for x in self.cd_stack]


	def emptyline (self) :
		return




def get_info_string( image ) :

	ret = ''
	ret += "Image Info:" + '\n'
	for k in meta_tags :
		if k != 'program' :
			ret += ( "	"+meta_templates[k]. format( image['meta'][k] ) ).encode('utf8') + '\n'
	return ret


if __name__ == "__main__" :		# TODO standalone module

	pass
