#-*- coding: utf-8 -*-

import cmd
from pprint import pprint 

class SatoriShell (cmd.Cmd) :

	commands = [ 'cd', 'ls', 'stat', 'cat', 'file', 'hash', 'pwd', 'info' ]
	debugs = [ 'keys', 'value' ]
	prompt = 'satori $ '

	# __image = None
	# __wd = None

	def __init__ (self, image) :
		cmd.Cmd.__init__(self)
		self.__image = image
		self.__wd = image['system']


	def exists (self, name) :
		if ( name in self.__wd['content'].keys() ) :
			return True
		else :
			print "File '%s' doesn't exist in current directory!" % name
			return False


	def do_ls (self, line) :
		if self.__wd['type'] == 'directory' :
			print "   ".join( self.__wd['content'].keys() )
		else :
			pprint( "'%s' is not a directory" % self.__wd )


	def do_cd (self, line) :
		f = line.strip()

		# print self.__wd['content'].keys()
		if f in self.__wd['content'].keys() :

			# print self.__wd['content'][f].keys()

			if self.__wd['content'][f]['type'] == 'directory' :
				self.__wd = self.__wd['content'][f]

			else :
				print "Can't 'cd' to '%s', not a directory." % self.__wd['content'][f]['filename']

		else :
			print "Can't 'cd' to '%s', directory doesn't exist." % f


	def do_stat (self, line) :

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
				print  "	%s : %s" % ( k, self.__wd[k] ) 

		return None


	def do__keys (self, line) :
		
		print self.__wd.keys()



if __name__ == "__main__" :		# TODO standalone module

	pass