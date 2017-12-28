#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.@q
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import sys

#
VALIDS = bx.reg('cmd.@q',{
		'y': 	True,
		'yes': 	True,
		'n': 	False,
		'no': 	False	
	})

#
def Q(n):
	if not bx._FLAG_SOURCE:
		return Q_prompt()
	return False

def Q_valid( value ):
	global VALIDS
	if value in VALIDS:
		if hasattr( VALIDS[value], '__call__' ):
			return VALIDS[value].__call__( value )
		else:
			return VALIDS[value]			
	return False

def Q_prompt( message = '' ):
	global VALIDS
	if message:
		message += ' '
		sys.stdout.write( message )
	try:
		while True:
			sys.stdout.write('[yes/no]? ')
			if sys.version_info < (3,0):
				choice = raw_input().lower()
			else:
				choice = input().lower()
			if choice in VALIDS:
				return Q_valid( choice )
	except:
		return False

def Q_if( name, value ):
	if value == 'true': return Q_prompt()
	return Q_prompt( value )

#
bx.reg.ex('bx.vars.get',{
		'@q': Q
	})

bx.reg.ex('bx.vars.set',{
		'@q': bx.var.readonly
	})

def __blox__():
	bx.reg.ex('cmd.if',{
			'@q': Q_if
		})

