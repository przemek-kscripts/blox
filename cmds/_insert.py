#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.insert
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def executor( PARSED, SOURCE = None ):
	PARSED.NAME = PARSED.arguments[0]
	BLOCK = bx.get( PARSED.NAME )
	if BLOCK:
		return BLOCK.run()
	else:
		bx.error('Insert for undefined block "%s"'%( PARSED.NAME ))
		return False

#
def __blox__():
	bx.cmd.reg({
			'insert': {
				'cmd.executor': executor,
				'args.min': 1,
				'args.max': 1
			}
		})