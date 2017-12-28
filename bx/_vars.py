#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx._vars
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import re
import os

#
_REXP_NAME = r'^([A-z\#\@\$\&][\w\#\@\$\&\.\-]*)$'
_REXP_FILTER = r'{(\@|\$|\#)\:'+_REXP_NAME[1:-1]+'}'
_VARS_GET = bx.reg('bx.vars.get')
_VARS_SET = bx.reg('bx.vars.set')
_VARS = bx.reg('bx.vars')

#
def FILTER( text ):
	match = re.search( _REXP_FILTER, text )
	if match:
		value = ''
		name = _name(match.group(2))
		if name:
			mode = match.group(1)
			if mode == '@' or mode == '#':
				value = _get( name )
			if mode == '$' or(mode == '@' and value is None):
				value = _env( name )
			value = var_str( value )
		return FILTER( 	text[:match.start()]+ 
						value+
						text[match.end():]
					)
	return text

#
def var( name, *value ):
	name = _name( name )
	if name:
		if value:
			if bx._FLAG_DEBUG:
				if name in _VARS_SET and _VARS_SET[ name ] != READONLY:
					bx.debug('Set "%s" to "%s"'%( name, var_str(value[0]) ))
			return _set( name, value[0] )
		else:
			return _get( name )
	else:
		return None

#
def _name( name ):
	if re.search( _REXP_NAME, name ):
		return name.lower()
	else:
		bx.error('Variable name "%s" syntax error'%(name))
	return None

def _set( name, value ):
	if name in _VARS_SET:
		if hasattr( _VARS_SET[ name ], '__call__' ):
			return _VARS_SET[ name ].__call__( name, value )
	_VARS[ name ] = value
	return _VARS[ name ]

def _get( name ):
	if name in _VARS_GET:
		if hasattr( _VARS_GET[ name ], '__call__' ):
			return _VARS_GET[ name ].__call__( name )
	if name in _VARS:
		return _VARS[ name ]
	return None

def _env( name ):
	return os.getenv( name )

#
def var_ist( name ):
	name = _name( name )
	if name:
		if name in _VARS:
			return True
		if name in _VARS_GET:
			return True
	return False

def var_set( name, value ):
	name = _name( name )
	if name:
		_VARS[ name ] = value
		return _VARS[ name ]
	return None

def var_get( name ):
	name = _name( name )
	if name in _VARS:
		return _VARS[ name ]
	return None

def var_env( name ):
	value = _env( name )
	if not value:
		name = _name( name )
		if name:
			value = os.getenv( name )
	return value

def var_str( value ):
	if value is False: return 'false'
	if value is True: return 'true'
	if value is None: return 'undefined'
	return str(value)

def var_val( string ):
	value = str(string).strip().lower()
	if value in ('false','off','disable'):
		return False
	if value in ('true','on','enable'):
		return True
	if value in ('undefined','none'):
		return None
	if value.isdigit():
		return int(value)
	try:
		return float(value)
	except:
		return str(string)

#
def READONLY( n, v ):
	bx.warning('Variable "%s" is only readonly'%(n))
	return v

#
bx.var = var
bx.var.readonly = READONLY
bx.var.filter = FILTER

#
var._ist = var_ist
var._set = var_set
var._get = var_get
var._env = var_env
var._str = var_str
var._val = var_val