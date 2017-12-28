#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.output
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx

#
def executor( PARSED, SOURCE ):
	output = bx.FILE.OUTPUT( PARSED.arguments[0] )
	bx.output( SOURCE.run() )
	bx.FILE.OUTPUT( output )

#
def __blox__():
	bx.cmd.reg({
			'output': {
				'cmd.executor': executor,
				'cmd.decisioner': True,
				'args.min': 1,
				'args.max': 1
			}
		})
