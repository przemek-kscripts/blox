#!python
# -*- coding: utf-8 -*-
"""
	@package: 	bx.FILE
	@author: 	KRZYSZTOF "@K0FF.EU" K0FF
	@version: 	2.17.12
"""
import bx
import os

_target = None
_outputs = {}
_checks = {}

def PATH( filepath, checkExists = True ):
	filepath = bx.unquote( filepath )
	if not filepath:
		bx.error('Invalid file path "%s"'%(filepath))
		return False
	if os.name == 'nt':
		filepath = filepath.lower()
	filepath = os.path.abspath( filepath )
	if os.path.isdir( filepath ):
		bx.error('Invalid file path "%s"'%(filepath))
		return False
	if checkExists:
		if not os.path.isfile( filepath ):
			bx.error('File "%s" not exists'%(filepath))
			return False 			
	return filepath

def LOAD( filepath, checkFilepath = True ):
	if checkFilepath:
		filepath = bx.FILE.PATH( filepath )
	if filepath:
		return open( filepath, 'r').read().splitlines()		
	bx.error('File dont loaded')
	return []

def IMPORT( filepath_short ):
	filepath = bx.FILE.PATH( filepath_short )
	if filepath:
		if filepath in _checks and _checks[ filepath ]:
			bx.error('Illegal recursion to file "%s"'%(filepath_short))
			return False
		else:
			if bx._FLAG_DEBUG:
				bx.debug('Import: "%s"'%(filepath_short))
		previous_input = bx.var._get('@input')
		bx.var._set( '@input', filepath_short )
		output = ''
		_checks[ filepath ] = True
		code = bx.FILE.LOAD( filepath, False )
		if code:
			CODE = bx.code( file=filepath_short, code=code )
			output = CODE.run()
		_checks[ filepath ] = False
		bx.var._set( '@input', previous_input )
		if not output:
			return False
		return output
	return False

def OUTPUT( filepath_short = None ):
	if filepath_short and bx._FLAG_DEBUG:
		bx.debug('Set current output: "%s"'%( filepath_short ))
	global _target
	bx.var._set( '@output', filepath_short )
	if filepath_short == None:
		_target,filepath = None,_target
		return filepath
	filepath = bx.FILE.PATH( filepath_short, False )
	if filepath == _target:
		return filepath
	if not filepath in _outputs:
		_outputs[ filepath ] = open( filepath, 'w' )
	filepath,_target = _target,filepath
	return filepath

def CLOSE():
	for filepath in _outputs:
		if bx._FLAG_DEBUG:
			bx.debug('Close file "%s"'%(filepath))
		_outputs[ filepath ].close()

def output( text ):
	if text and _target:
		if bx._FLAG_DEBUG:
			bx.debug('Outpud saved to "%s"'%(bx.var('@output')))
		_outputs[ _target ].write( text )

#
def SET_OUTPUT( name, value ):
	bx.FILE.OUTPUT( value )
	
#
bx.reg.ex('bx.vars.set',{
		'@output': SET_OUTPUT,
	})

#
bx.output = output
