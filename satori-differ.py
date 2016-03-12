#!/usr/bin/python
#-*- coding: utf-8 -*-

import platform as plat

import logging as log
import argparse

import lib.image_differ as differ
import lib.image_io as io
import lib.definitions as defs


header = '''
Welcome to {0} Differ
OS filesystem image Difference Finder
Version {1}
'''.format(defs.program_name, defs.version)


log.basicConfig(format = "%(message)s")

__log = log.getLogger( __name__ )



if __name__ == "__main__" :

	os_def_name = plat.platform()

	parser = argparse.ArgumentParser( description = 'Crawls the whole filesystem and creates an image of it to a file.' )
