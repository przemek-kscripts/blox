#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmds
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import os
_MODULES = []

def init():
	for name in os.listdir(bx.PATH+"/cmds"):
		if not name == "__init__.py" and name.endswith(".py"):
			name = name[:-3]
			__import__("cmds."+ name )
			_MODULES.append( globals()[name] )
			bx.var( '@cmd.'+name, True )
#
def load():
	for module in _MODULES:
		if hasattr( module, "__blox__" ):
			module.__blox__()