#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.exec
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import os

"""
exec:{@:command}
exec:print:{@:command}
exec:write:{@:command}
exec:cls
"""

#
def EXEC_call( PARSED ):
	os.system( PARSED.COMMAND )
	return False

def EXEC_print( PARSED ):
	wrapper = os.popen(PARSED.COMMAND)
	results = os.popen(PARSED.COMMAND).read()
	wrapper.close()
	if results and results[-1] == '\n':
		results = results[:-1]
	if results:
		if PARSED.RECIVER == 'print':
			bx.write(results)
		if PARSED.RECIVER != 'null':
			return results
	return False

def EXEC_cls( PARSED ):
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	return False

#
CMDS = bx.reg('cmd.exec.command',['cls'])
EXEC = bx.reg('cmd.exec',{
		'call': EXEC_call,
		'null': EXEC_print,
		'print': EXEC_print,
		'hide': EXEC_print,
		'cls': EXEC_cls
	})

#
def decisioner( PARSED ):
	if PARSED.length == 1:
		PARSED.COMMAND = PARSED.arguments[0]
		if PARSED.COMMAND.lower() in CMDS:
			PARSED.COMMAND = PARSED.COMMAND.lower()
			PARSED.RECIVER = PARSED.COMMAND
		else:
			PARSED.RECIVER = 'call'
		return False

	PARSED.RECIVER = PARSED.arguments[0].lower()
	PARSED.COMMAND = PARSED.arguments[1]

	if not PARSED.RECIVER in EXEC:
		bx.error('Unknown cmd.exec reciver: "exec:%s"'%(PARSED.RECIVER))

	return False


def executor( PARSED, SOURCE = None ):
	if bx._FLAG_DEBUG:
		bx.debug('Execute "%s" on "%s"'%(PARSED.COMMAND,PARSED.RECIVER))
	return EXEC[ PARSED.RECIVER ].__call__( PARSED )

#
def __blox__():
	bx.cmd.reg({
			'exec': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'args.min': 1,
				'args.max':2
			}
		})
