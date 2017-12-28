#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx._regs
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
_REGS = {}

#
def reg( name, ex = None ):
	if not name in _REGS: _REGS[name] = {}
	if ex:
		if type(ex) == dict:
			for key in ex: _REGS[name][key] = ex[key]
		elif type(ex) == list:
			for key in ex: _REGS[name][key] = True
		else:
			_REGS[name] == ex
	return _REGS[name]

#
reg.ex = reg
bx.reg = reg