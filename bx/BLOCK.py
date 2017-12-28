#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx.BLOCK
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import re
_REXP_NAME = r'^([A-z\#\@\$\&][\w\#\@\$\&\.\-]*)$'
_BLOCKS = {}

#
def _name( name ):
	if re.search( _REXP_NAME, name ):
		return name.lower()
	else:
		bx.error('Block name "%s" syntax error'%(name))	

#
def set( name, SOURCE ):
	name = _name( name )
	if name:
		if name in _BLOCKS:
			_BLOCKS[name]._name = None
			bx.debug('Redefined block "%s"'%(name))
		else:
			bx.debug('Define block "%s"'%(name))
		SOURCE._name = name
		_BLOCKS[name] = SOURCE
		return _BLOCKS[name]
	return bx.code()

def get( name ):
	name = _name( name )
	if name and name in _BLOCKS:
		return _BLOCKS[name]
	return bx.code()

#
bx.set = set
bx.get = get