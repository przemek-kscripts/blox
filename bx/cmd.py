#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx.cmd
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import cmds
_ALIAS = {}
_BLOCK = {
	'end': True,
	'break': True,
	'halt': True,
	';': True
}

#
def init():
	cmds.init()

def load():
	cmds.load()
#
def reg( commands ):
	for name in commands:
		_BLOCK[name] = commands[name]
		if commands[name] == True:
			continue
		keys = commands[name].keys()

		if not 'cmd.executor' in keys:
			commands[name]['cmd.executor'] = True

		if 'cmd.alias' in keys:
			reg_alias( name, commands[name]['cmd.alias'] )

def reg_alias( command, aliases ):
	if type(aliases) == str:
		_ALIAS[aliases] = command
	else:
		for alias in aliases:
			_ALIAS[alias] = command
#
def isCommand( command ):
	if command in _ALIAS:
		command = _ALIAS[command]
	if command in _BLOCK:
		return command
	bx.error('Unknown command: "%s"'%(command))
	return False

def isBlock( PARSED ):
	if PARSED.command in _BLOCK:
		if _BLOCK[PARSED.command] == True:
			return False
		if 'cmd.decisioner' in _BLOCK[PARSED.command]:
			if hasattr( _BLOCK[ PARSED.command ]['cmd.decisioner'], '__call__' ):
				return _BLOCK[ PARSED.command ]['cmd.decisioner'].__call__( PARSED )
			else:
				return bool(_BLOCK[ PARSED.command ]['cmd.decisioner'])		
	return False
#
def execute( PARSED, SOURCE = None ):
	if PARSED.arguments:
		PARSED.length = len(PARSED.arguments)
	else:
		PARSED.length = 0

	if PARSED.command in _BLOCK:
		if _BLOCK[ PARSED.command ] == True:
			return False

		if 'args.max' in _BLOCK[ PARSED.command ]:
			if PARSED.length > _BLOCK[ PARSED.command ]['args.max']:
				bx.error('Command "%s" accept less arguments (max:%d)'%(
						PARSED.command,
						_BLOCK[ PARSED.command ]['args.max'] )
					)
				return False

		if 'args.min' in _BLOCK[ PARSED.command ]:
			if PARSED.length < _BLOCK[ PARSED.command ]['args.min']:
				bx.error('Command "%s" require many arguments (min:%d)'%(
						PARSED.command, 
						_BLOCK[ PARSED.command ]['args.min'] )
					)
				return False

		if hasattr( _BLOCK[ PARSED.command ]['cmd.executor'], '__call__' ):
			return _BLOCK[ PARSED.command ]['cmd.executor']( PARSED, SOURCE )
			
	else:
		bx.error('Unknown command: "%s"'%(parsed.command))
	return False
