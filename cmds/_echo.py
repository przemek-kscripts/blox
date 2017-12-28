#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.echo
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def ECHO_error( message ):
	bx.error( message )
	bx.running = True

#
ECHO = bx.reg('cmd.echo',{
		'message':	bx.message,
		'debug': bx.debug,
		'error': ECHO_error,
		'warning': bx.warning,
		'write': bx.write,
		'print': lambda x: x,
		'output': bx.output,
		'notice': bx.notice
	})

#
def decisioner( PARSED ):
	if PARSED.length == 0:
		if PARSED.alias:
			PARSED.RECIVER = PARSED.alias
		else:
			PARSED.RECIVER = 'message'
		return True

	if PARSED.length == 1:
		if PARSED.alias:
			PARSED.RECIVER = PARSED.alias
			PARSED.MESSAGE = PARSED.arguments[0]
		else:
			PARSED.RECIVER = PARSED.arguments[0].lower()
			if PARSED.RECIVER in ECHO:
				return True
			else:
				PARSED.RECIVER = 'message'
				PARSED.MESSAGE = PARSED.arguments[0]
				return False
	else:
		PARSED.RECIVER = PARSED.arguments[0].lower()
		PARSED.MESSAGE = PARSED.arguments[1]
		
	if not PARSED.RECIVER in ECHO:
		bx.error('Unknown cmd.echo reciver: "echo:%s"'%(PARSED.RECIVER))
	#
	return False

def executor( PARSED, SOURCE ):
	if PARSED.isBlock:
		output = ''
		for line in SOURCE:
			result = ECHO[PARSED.RECIVER].__call__(line)
			if result:
				if output: output += '\n'
				output += result
		if output:
			return output
	else:
		if PARSED.MESSAGE == '.': PARSED.MESSAGE = ''
		return ECHO[PARSED.RECIVER].__call__(
				PARSED.MESSAGE
			)

#
def __blox__():
	bx.reg('cmd.code.ungrabbable',{
			'echo': True,
			'write': True,
			'print': True
		})
	
	bx.cmd.reg({
			'echo': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'cmd.alias': ['write','print'],
				'args.max': 2
			}
		})