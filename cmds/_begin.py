#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.begin
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def BEGIN_create( PARSED, SOURCE ):
	bx.BLOCK.set( PARSED.NAME, SOURCE )
	return SOURCE.run()

def BEGIN_define( PARSED, SOURCE ):
	bx.BLOCK.set( PARSED.NAME, SOURCE )
	return False

#
BEGIN = bx.reg('cmd.begin',{
		'create': BEGIN_create, 
		'define': BEGIN_define,
	})

#
def decisioner( PARSED ):
	PARSED.NAME = PARSED.arguments[0] 
	if PARSED.length == 1:
		PARSED.RECIVER = 'create'
	else:
		PARSED.RECIVER = PARSED.arguments[1].lower()
	if not PARSED.RECIVER in BEGIN:
		bx.error('Unknown cmd.begin reciver: "begin:%s"'%(PARSED.RECIVER))
	return True

def executor( PARSED, SOURCE ):
	return BEGIN[PARSED.RECIVER].__call__( PARSED, SOURCE )		

#
def __blox__():
	bx.cmd.reg({
			'begin': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'args.min': 1,
				'args.max': 2
			}
		})