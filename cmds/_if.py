#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.if
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
IF = bx.reg('cmd.if')

#
def decisioner( PARSED ):
	if PARSED.length > 1:
		PARSED.VALUE = bx.var._val( PARSED.arguments[1] )
	else:
		PARSED.VALUE = True

	if PARSED.length:
		PARSED.NAME = PARSED.arguments[0].lower()
	
	if not PARSED.alias:
		PARSED.alias = 'when'
	return True

def executor( PARSED, SOURCE ):
	if PARSED.NAME in IF:
		value = IF[PARSED.NAME]( PARSED.NAME, PARSED.VALUE )
	else:
		value = bx.var(PARSED.NAME)
		if PARSED.VALUE is True or PARSED.VALUE is False:
			value = PARSED.VALUE == bool(value)
		else:
			value = PARSED.VALUE == value

	if (PARSED.alias == 'when') == value:
		return SOURCE.run()

	return False

#
def __blox__():
	bx.cmd.reg({
			'if': {
				'cmd.executor': executor,
				'cmd.decisioner': decisioner,
				'cmd.alias': ['when','else'],
				'args.min': 1,
				'args.max': 2
			}
		})	