#!python
# -*- coding: utf-8 -*-
"""
	@program: 	BLOX
	@author: 	KRZYSZTOF "@K0FF.EU" K0FF
	@version: 	2.17.12
	@license: 	X11
"""
import bx
import bx._regs
import bx._vars
import bx.BLOCK
import bx._parser
import bx._echo
import bx.CODE
import bx.FILE
import bx.cmd
import time

#
def unquote( text, striped = False ):
	if not striped:
		text = text.strip()
	if len(text) and text[0] == '\"' and text[-1] == '\"':
		return text[1:-1]
	return text

#
def reset():
	bx.timed = time.time()
	bx.running = True
	bx.errors = 0
	bx.warnings = 0
	bx.depth = 0

#
def init():
	bx.cmd.init()

def load():
	bx.cmd.load()

#
def status():
	if bx._FLAG_ECHO or bx._FLAG_DEBUG or not bx.running:
		bx.color( 'reset', '\n' )
		bx.color( 'warning', 'Warnings: %s'%(bx.warnings) )
		bx.write( 'Time: %s sec.'%(str(round((time.time()-timed),3))) )

		if bx.errors:
			bx.color( 'error', 'Errors: %s'%(bx.errors) )

		if bx.running:
			bx.color( 'SOURCE', 'Success.\n')
		else:
			if bx._FLAG_HALTED:
				bx.color( 'error', 'Stopped.\n')
			else:
				bx.color( 'error', 'Halted.\n')
