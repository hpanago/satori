import logging

crit_fmt = "[ ! ] %(msg)s"
err_fmt = "[+] %(msg)s"
warn_fmt = "[*] %(msg)s"
info_fmt = "[-] %(msg)s"

dbg_fmt = "[@]: %(module)s: %(lineno)d: %(msg)s"

class CustomFormatter (logging.Formatter) :
	    def __init__(self, fmt = '%(message)s'):
        logging.Formatter.__init__(self, fmt)

        def format(self, record):
        if record.levelno == logging.INFO:
        	# inf = 
        return logging.Formatter.format(record)