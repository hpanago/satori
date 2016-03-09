
import cPickle as pickle
import json

def loadImage(filename, type = 'pickle') :
	infile = open(filename, 'r')
	meth = pickle
	if type == 'json' :
		meth = json

	meth.load ( infile )


def saveImage(filename, toSave, type = 'pickle') :
	outfile = open(filename, 'w')
	meth = pickle
	if type == 'json' :
		meth = json

	outfile.write( meth.dumps( toSave ) ) 

