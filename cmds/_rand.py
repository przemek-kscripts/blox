#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.@rand
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import random

RAND_MIN = 1
RAND_MAX = 6

#
def RAND( name ):
	a = min( RAND_MIN, RAND_MAX ) 
	b = max( RAND_MIN, RAND_MAX )
	return random.randint( a, b )

def RAND_set( name, value ):
	global RAND_MIN
	global RAND_MAX
	if name == '@rand.min':
		try:
			RAND_MIN = int( value )
		except:
			bx.error('%s value (%s) is not number'%( name, value ))
	elif name == '@rand.max':
		try:
			RAND_MAX = int( value )
		except:
			bx.error('%s value (%s) is not number'%( name, value ))
	if bx._FLAG_DEBUG:
		p = abs( RAND_MAX - RAND_MIN + 1 )
		bx.debug('Probality set 1:%d'%(p))
	return value

def RAND_if( name, value ):
	global RAND_MIN
	value = bx.var._val( value )
	if type(value) == bool:
		return bx.var('@rand') == RAND_MIN
	else:
		return bx.var('@rand') == value

def RAND_q( name ):
	if name == '?':
		value = bool(bx.var('@rand')%2)
	else:
		value = bx.var('@rand.min') == bx.var('@rand')
	bx.notice('Random choice: %s'%(bx.var._str(value)))
	return value

#
bx.reg.ex('bx.vars.set',{
		'@rand': bx.var.readonly,
		'@rand.min': RAND_set,
		'@rand.max': RAND_set
	})

bx.reg.ex('bx.vars.get',{
		'@rand': RAND,
		'@rand.min': lambda n: RAND_MIN,
		'@rand.max': lambda n: RAND_MAX
	})

#
def __blox__():
	bx.reg.ex('cmd.if',{
		'@rand': RAND_if
	})

	bx.reg.ex('cmd.@q',{
		'?': RAND_q,
		'@': RAND_q
	})

