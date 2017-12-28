#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.file
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import glob
import os.path
import bx

#
def FILE_get( name ):
	if not bx._FLAG_SOURCE:

		if name == '#file':
			filepath = bx.var._get('#file')
			if not filepath:
				filepath = bx.var('@input')
			return filepath

		name = name.split('.',1)
		filepath = bx.var(name[0])
		if not filepath: return filepath
		filepath = os.path.abspath( filepath )

		if name[1] == "name":
			return os.path.basename( filepath )

		elif name[1] == "path":
			return filepath

		elif name[1] == "isdir":
			return os.path.isdir( filepath )

		elif name[1] in ("dir","directory"):
			return os.path.dirname( filepath )

		elif name[1] in ("ext","extension"):
			return os.path.splitext(filepath)[1][1:]

		elif name[1] == "base":
			filepath = os.path.basename( filepath )
			return os.path.splitext(filepath)[0]

#
def NAME( namebase ):
	bx.reg.ex('bx.vars.set',{
			namebase+'.name': bx.var.readonly,
			namebase+'.path': bx.var.readonly,
			namebase+'.isdir': bx.var.readonly,
			namebase+'.dir': bx.var.readonly,
			namebase+'.directory': bx.var.readonly,
			namebase+'.extension': bx.var.readonly,
			namebase+'.ext': bx.var.readonly,
			namebase+'.base': bx.var.readonly,
		})

	bx.reg.ex('bx.vars.get',{
			namebase+'.name': FILE_get,
			namebase+'.path': FILE_get,
			namebase+'.isdir': FILE_get,
			namebase+'.dir': FILE_get,
			namebase+'.directory': FILE_get,
			namebase+'.extension': FILE_get,
			namebase+'.ext': FILE_get,
			namebase+'.base': FILE_get,
		})

#
def FILE_import( PARSED ):
	for FILEPATH in glob.glob(PARSED.PATTERN):
		bx.FILE.IMPORT( FILEPATH )
	return False

def FILE_include( PARSED ):
	output = ''
	for FILEPATH in glob.glob(PARSED.PATTERN):
		result = bx.FILE.IMPORT( FILEPATH )
		if result:
			output += result
	if output:
		return output
	return False

#
def FILE_loop( PARSED, SOURCE ):
	output = ''
	for FILEPATH in glob.glob(PARSED.PATTERN):
		if bx._FLAG_DEBUG:
			bx.debug('FILELOOP: (%s|%s)'%(FILEPATH,PARSED.PATTERN))
		previous_file = bx.var._get( '#file' )
		bx.var._set( '#file', FILEPATH )
		result = SOURCE.run()
		if result:
			output += result + '\n'
		if not bx.running:
			break
		bx.var._set( '#file', previous_file )
	if bx._FLAG_DEBUG:
			bx.debug('FILELOOP: END;')
	if output:
		return output
	else:
		return False

#
CODE = bx.reg('cmd.file.code',['loop'])
FILE = bx.reg('cmd.file',{
		'import': FILE_import,
		'include': FILE_include,
		'loop': FILE_loop
	})

#
bx.reg.ex('bx.vars.get',{
		'#file': FILE_get
	})

#
NAME('@input')
NAME('@output')
NAME('#file')

#
def decisioner( PARSED ):
	if PARSED.length == 1:
		if PARSED.alias:
			PARSED.arguments.insert( 0, PARSED.alias )
		else:
			PARSED.arguments.insert( 0, 'import' )

	PARSED.RECIVER = PARSED.arguments[0].lower()
	PARSED.PATTERN = PARSED.arguments[1]

	if not PARSED.RECIVER in FILE:
		bx.error('Unknown cmd.file reciver: "file:%s"'%(PARSED.RECIVER))

	return PARSED.RECIVER in CODE

def executor( PARSED, SOURCE = None ):
	if SOURCE is None:
		return FILE[ PARSED.RECIVER ].__call__( PARSED )
	else:
		return FILE[ PARSED.RECIVER ].__call__( PARSED, SOURCE )

#
def __blox__():
	bx.cmd.reg({
			'file': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'cmd.alias': ['import','include'],
				'args.min': 1,
				'args.max': 2
			}
		})