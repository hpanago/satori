import logging

crit_fmt = "[ ! ] %(msg)s"
err_fmt = "[+] %(msg)s"
warn_fmt = "[*] %(msg)s"
info_fmt = "[-] %(msg)s"

dbg_fmt = "[@]: %(module)s: %(lineno)d: %(msg)s"

'''
\[\033[1;34m\][\$(date +%H%M)][\u@\h:\w]$\[\033[0m\]
Black       0;30     Dark Gray     1;30
Blue        0;34     Light Blue    1;34
Green       0;32     Light Green   1;32
Cyan        0;36     Light Cyan    1;36
Red         0;31     Light Red     1;31
Purple      0;35     Light Purple  1;35
Brown       0;33     Yellow        1;33
Light Gray  0;37     White         1;37
'''

class CustomFormatter (logging.Formatter) :
	def __init__(self, fmt = '%(message)s'):
		logging.Formatter.__init__(self, fmt)

	def format(self, record):
		# if record.levelno == logging.INFO:
			# inf = 
		return logging.Formatter.format(record)