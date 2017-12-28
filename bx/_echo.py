#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx._echo
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import sys
import os

#
def POSITION():
	message = ''
	if bx.CODE._line:
		message += ' on line '+str(bx.CODE._line)
	if bx.CODE._name:
		message += ' in block "%s"'%(bx.CODE._name)
	if bx.CODE._file:
		message += ' in file "%s"'%(bx.CODE._file)
	return message

#
def COLOR():
	if 'CONEMUANSI' in os.environ:
		if 'ON' in os.environ['CONEMUANSI']:
			return True
		else:
			return False
	if sys.platform == 'win32':
		return False
	return True

#
bx._COLOR_MESSAGE = ''
bx._COLOR_DEBUG = '\033[94m'
bx._COLOR_WARNING = '\033[93m'
bx._COLOR_ERROR = '\033[91m'
bx._COLOR_NOTICE = '\033[94m'
bx._COLOR_RESET = '\033[0m'

#
def SET_COLOR( name, value ):
	if name == '@color.message': bx._COLOR_MESSAGE = value
	elif name == '@color.debug': bx._COLOR_DEBUG = value
	elif name == '@color.warning': bx._COLOR_WARNING = value
	elif name == '@color.error': bx._COLOR_ERROR = value
	elif name == '@color.notice': bx._COLOR_NOTICE = value
	elif name == '@color.reset': bx._COLOR_RESET = value
	return value

#
bx._FLAG_COLOR = COLOR()
bx._FLAG_ECHO = False
bx._FLAG_WARNING = True
bx._FLAG_DEBUG = False

#
def SET_FLAG( name, value ):
	if name == '@color': bx._FLAG_COLOR = bool(value)
	elif name == '@echo': bx._FLAG_ECHO = bool(value)
	elif name == '@warning': bx._FLAG_WARNING = bool(value)
	elif name == '@debug': 
		bx._FLAG_DEBUG = bool(value)
		if bx._FLAG_DEBUG: bx.debug('ENABLED')
	return value

#
bx.reg.ex('bx.vars.get',{
		'@color': lambda n: bx._FLAG_COLOR,
		'@color.message': lambda n: bx._COLOR_MESSAGE,
		'@color.debug': lambda n: bx._COLOR_DEBUG,
		'@color.warning': lambda n: bx._COLOR_WARNING,
		'@color.error': lambda n: bx._COLOR_ERROR,
		'@color.notice': lambda n: bx._COLOR_NOTICE,
		'@color.reset': lambda n: bx._COLOR_RESET,
		'@echo': lambda n: bx._FLAG_ECHO,
		'@warning': lambda n: bx._FLAG_WARNING,
		'@debug': lambda n: bx._FLAG_DEBUG
	})

bx.reg.ex('bx.vars.set',{
		'@color': SET_FLAG,
		'@color.message': SET_COLOR, 
		'@color.debug': SET_COLOR, 
		'@color.warning': SET_COLOR, 
		'@color.error': SET_COLOR, 
		'@color.notice': SET_COLOR, 
		'@color.reset': SET_COLOR, 
		'@echo': SET_FLAG,
		'@warning': SET_FLAG,
		'@debug': SET_FLAG
	})

#
def color( name, message = '' ):
	if message:
		if bx._FLAG_COLOR:
			color = bx.var('@color.'+name )
			if color: 
				message = color + message + bx._COLOR_RESET
		sys.stdout.write( message + '\n' )
	else:
		if bx._FLAG_COLOR:
			color = bx.var('@color.'+name )
			if color:
				sys.stdout.write( color )

#
def message( message ):
	if bx._FLAG_ECHO:
		message = 'Message: "' + message + '"' + POSITION()
	if bx._FLAG_COLOR:
		message = bx._COLOR_MESSAGE + message + bx._COLOR_RESET
	sys.stdout.write( message +'\n' )

def debug( message ):
	if bx._FLAG_DEBUG:
		message = 'Debug: ' + message + POSITION()
		if bx._FLAG_COLOR:
			message = bx._COLOR_DEBUG + message + bx._COLOR_RESET
		sys.stdout.write( message +'\n' )

def notice( message ):
	if bx._FLAG_DEBUG:
		message = 'Notice: '+ message
	if bx._FLAG_ECHO:
		message += POSITION()
	if bx._FLAG_COLOR:
		message = bx._COLOR_NOTICE + message + bx._COLOR_RESET
	sys.stdout.write( message +'\n' )

def warning( message ):
	message = 'Warning: ' + message + POSITION()
	if bx._FLAG_COLOR:
		message = bx._COLOR_WARNING + message + bx._COLOR_RESET
	sys.stdout.write( message +'\n' )
	bx.warnings += 1

def error( message ):
	message = 'Error: ' + message + POSITION()
	if bx._FLAG_COLOR:
		message = bx._COLOR_ERROR + message + bx._COLOR_RESET
	sys.stderr.write( message +'\n' )
	bx.running = False
	bx.errors += 1

def write( message ):
	sys.stderr.write( message +'\n' )

#
bx.color = color
bx.message = message
bx.debug = debug
bx.notice = notice
bx.warning = warning
bx.error = error
bx.write = write