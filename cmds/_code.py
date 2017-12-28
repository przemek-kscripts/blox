#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.code
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def CODE_skip( PARSED, SOURCE ):
	return False

def CODE_remove( PARSED, SOURCE ):
	SOURCE.run()
	return False

def CODE( PARSED, SOURCE ):
	if not bx._FLAG_CODEMODE:
		SOURCE = SOURCE.compile()
	bx.bx._FLAG_CODEMODE = True
	output = SOURCE.run()
	bx._FLAG_CODEMODE = False
	return output

#
GRAB = bx.reg('cmd.code.ungrabbable')
CODE = bx.reg('cmd.code',{
		'skip': CODE_skip,
		'remove': CODE_remove,
		'code': CODE
	})

#
def decisioner( PARSED ):
	if PARSED.length == 0:
		if PARSED.alias:
			PARSED.RECIVER = PARSED.alias
		else:
			PARSED.RECIVER = 'code'
		return True
	else:
		PARSED.RECIVER = PARSED.arguments[0].lower()

	if not PARSED.RECIVER in CODE:
		bx.error('Unknown cmd.code reciver: "code:%s"'%(PARSED.RECIVER))
	return True

def executor( PARSED, SOURCE ):
	return CODE[PARSED.RECIVER].__call__( PARSED, SOURCE )

#
def __blox__():
	bx.cmd.reg({
			'code': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'cmd.alias': ['skip','remove'],
				'args.max': 1
			}
		})