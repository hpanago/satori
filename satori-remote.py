#!/usr/bin/python

#-*- coding: utf-8 -*-

import platform as plat
import os

import logging as log
import argparse

import paramiko
from paramiko import SSHClient
#from lib.helpers.paramiko_sftp_recursive import RecursiveSFTPClient
from scpclient import closing, WriteDir
# from scp import SCPClient
import getpass


import lib.image_maker as maker
import lib.image_io as io
import lib.definitions as defs

import lib.helpers.signal_handler

import signal
import sys


header = defs.header.format( "OS Remote filesystem image Creator via SSH" )

log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



if __name__ == "__main__" :


	parser = argparse.ArgumentParser( description = 'Creates a Satori image from a remote OS using SSH' )

	parser.add_argument( 'user_host', metavar = 'USER@HOSTNAME|HOSTNAME',\
		help = 'The user and host to connect and run the satori-imager.py' )

	parser.add_argument('--arguments', '-args',\
		help = '''The whole argument string to pass to remote 'satori-imager.py'. 
				 For help on those arguments type "satori-imager.py -h"''',\
		default = '--threads 2' )

	parser.add_argument( '--key', '-i', help = 'SSH Key to connect', default = None )

	parser.add_argument( '--password', '-p',\
		help = '''SSH password. Avoid this option, as the password will be shown in bash history and 
				'ps' command''')

	parser.add_argument( '--not-purge', help = 'Do not purges the Satori files from target machine when finished',\
		action = 'store_false', default = True )

	parser.add_argument( '--r-dir', help = 'Directory to copy the Satori files in the remote host',\
		default = '/tmp/' )


	args = parser.parse_args()
	print args

	if not args.password :
		ssh_pass = getpass.getpass()
	else :
		ssh_pass = args.password


	remote_dir = args.r_dir
	arguments = args.arguments

	satoriFolder =  sys.path[0]
	print satoriFolder

	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 


	user = None
	if '@' in args.user_host :
		user = args.user_host.split('@')[0]
		host = args.user_host.split('@')[1]

	else :
		host = args.user_host

	print args.user_host
	print user, host
	ssh.connect( host, username = user, password = ssh_pass, key_filename = args.key )



	sftp = ssh.open_sftp()

	# sftp = RecursiveSFTPClient( ssh.channel )


	with closing(WriteDir (ssh.get_transport(), remote_dir )) as scp:
		scp.send_dir( satoriFolder , preserve_times = True)
	# sftp.put_dir( satoriFolder, remote_dir )


	remote_satori = remote_dir + '/satori'
	old_contents = sftp.listdir( remote_satori )
	print old_contents

	rem_command = 'chmod 775 {0}; cd {0}; ./satori-imager.py {1} 2>&1 |tee /tmp/satori.log'. format( remote_satori, arguments )
	print rem_command
	stdin, stdout, stderr = ssh.exec_command( rem_command )
	print 'executing...'
	exit_status = stdout.channel.recv_exit_status()
	print exit_status


	new_contents = sftp.listdir( remote_satori )
	print new_contents

	output = list(set(new_contents) - set(old_contents))[0]

	if len(output) == 0 :
		print 'No output file. Something went wrong'
		sftp.close()
		ssh.close()
		sys.exit(1)

	localfile = os.getcwd() + '/' +output
	print localfile
	remotefile = remote_satori + '/' + output

	sftp.get( remotefile, localfile )

	sftp.close()
	print "Done!"

	if not args.not_purge :
		stdin, stdout, stderr = ssh.exec_command( 'rm -rf %s/satori' % remote_dir ) 
		exit_status = stdout.channel.recv_exit_status()


	ssh.close()




