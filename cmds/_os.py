#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.@os
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import sys
import os

#
def OS():
	if sys.platform in ('linux','linux2'): return 'linux'
	if sys.platform in ('win32','win64','cygwin'): return 'windows'
	if sys.platform == 'darwin': return 'darwin'
	return os.name

#
bx.var._set('@os',OS())

#
def OS_if( name, value ):
	OS = bx.var._get('@os')
	if value is True: return True
	if value is False: return False
	value = bx.var._str(value).lower()

	if value in ('windows','win'): return OS == 'windows'
	if value in ('darwin','macos','mac'): return OS == 'darwin'
	if value == 'linux': return OS == 'linux'

	if value == os.name: return True
	if value == sys.platform: return True
	return False

#
bx.reg.ex('bx.vars.set',{
		'@os': bx.var.readonly,
	})

#
def __blox__():
	bx.reg.ex('cmd.if',{
			'@os': OS_if
		})
