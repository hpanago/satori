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




def main():

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
		action = 'store_true', default = False )

	parser.add_argument( '--r-dir', help = 'Directory to copy the Satori files in the remote host',\
		default = '/tmp/' )

	verb = parser.add_mutually_exclusive_group()
	verb.add_argument( '--verbose', '-v' , help = 'verbose mode', action = 'count', default = 0 )
	verb.add_argument( '--debug' , '-d', help = 'debugging mode', action = 'store_true', default = False )
	verb.add_argument( '--quiet', '-q' , help = 'quiet mode', action = 'store_true', default = False )

	__log.warning(header)

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




	if not args.password :
		ssh_pass = getpass.getpass()
	else :
		__log.info("Password provided!")
		ssh_pass = args.password


	remote_dir = args.r_dir
	arguments = args.arguments

	__log.info( "Remote directory is '%s'" % remote_dir )

	satoriFolder =  sys.path[0]
	__log.info( "Satori will be copied from '%s'" % satoriFolder )


	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

	user = None
	if '@' in args.user_host :
		user = args.user_host.split('@')[0]
		host = args.user_host.split('@')[1]

	else :
		host = args.user_host

	__log.info ("Attempting SSH connection to '{0}' as user '{1}'".format( host, user ) )
	ssh.connect( host, username = user, password = ssh_pass, key_filename = args.key )
	__log.warning ("Connection Established!")
	sftp = ssh.open_sftp()
	__log.info ("SFTP channel opened!")
	# sftp = RecursiveSFTPClient( ssh.channel )


	with closing(WriteDir (ssh.get_transport(), remote_dir )) as scp:
		scp.send_dir( satoriFolder , preserve_times = True)
	__log.info ( "Satori folder copied at remote location '%s'" % remote_dir )
	# sftp.put_dir( satoriFolder, remote_dir )


	remote_satori = remote_dir + '/satori'
	old_contents = sftp.listdir( remote_satori )
	__log.debug( old_contents )

	rem_command = 'chmod 775 {0}; cd {0}; ./satori-imager.py {1} '. format( remote_satori, arguments )
	# rem_command = 'chmod 775 {0}; cd {0}; ./satori-imager.py {1} 2>&1 |tee /tmp/satori.log'. format( remote_satori, arguments )

	__log.info( "The command to run in remote host is:" )
	__log.info( "'%s'" % rem_command )

	stdin, stdout, stderr = ssh.exec_command( rem_command )

	__log.warning( "Executing... ")


	__log.info( "Output from Remote Execution:" )
	__log.info( "===========================================")
	__log.info( defs.bash_l_gray )

	for line in iter(lambda: stderr.readline(2048), ""):
		__log.info( line[:-1] )	# last char is the next_line

	__log.info( defs.bash_n_color )
	__log.info( "===========================================")

	exit_status = stdout.channel.recv_exit_status()

	new_contents = sftp.listdir( remote_satori )
	__log.debug( new_contents )

	output = list(set(new_contents) - set(old_contents))[0]


	if len(output) == 0 :
		__log.critical( 'No output file. Something went wrong. Exiting...' )
		sftp.close()
		ssh.close()
		sys.exit(1)

	localfile = os.getcwd() + '/' +output
	remotefile = remote_satori + '/' + output

	i = 1
	new_localfile = localfile

	while os.path.exists( new_localfile ) :
		new_localfile = localfile + '_' + str(i)
		i += 1

	localfile = new_localfile

	__log.info( "Getting remote file '%s'" % remotefile )
	sftp.get( remotefile, localfile )

	sftp.close()
	__log.warning( "Done!")
	__log.warning("Satori image is located at '%s'" % localfile )

	if not args.not_purge :
		stdin, stdout, stderr = ssh.exec_command( 'rm -rf %s' % remote_satori ) 
		exit_status = stdout.channel.recv_exit_status()
		__log.info( "Remote copied files purged!" )



	ssh.close()
	__log.info( "SSH session closed!" )


if __name__ == "__main__" :
    main()
