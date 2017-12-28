#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.var
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def VAR_set( PARSED ):
	bx.var( PARSED.NAME, bx.var._val(PARSED.VALUE) )
	return False

def VAR_def( PARSED ):
	if not bx.var._ist( PARSED.NAME ):
		bx.var( PARSED.NAME, bx.var._val(PARSED.VALUE) )
	return False

#
VAR = bx.reg('cmd.var',{
		'set': VAR_set,
		'def': VAR_def
	})

#
def decisioner( PARSED ):
	if PARSED.length == 2:
		if PARSED.alias:
			PARSED.arguments.insert(0,PARSED.alias)
		else:
			PARSED.arguments.insert(0,'set')

	PARSED.RECIVER = PARSED.arguments[0].lower()
	PARSED.NAME = PARSED.arguments[1]
	PARSED.VALUE = PARSED.arguments[2]

	if not PARSED.RECIVER in VAR:
		bx.error('Unknown cmd.var reciver: "var:%s"'%(PARSED.RECIVER))
	return False

def executor( PARSED, SOURCE = None ):
	return VAR[ PARSED.RECIVER ]( PARSED )

#
def __blox__():
	bx.cmd.reg({
			'var': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'cmd.alias': ['set','def'],
				'args.min': 2,
				'args.max': 3
			}
		})