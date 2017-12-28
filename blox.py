#!python
# -*- coding: utf-8 -*-
"""
	@program: 	BLOX
	@author: 	KRZYSZTOF "@K0FF.EU" K0FF
	@version: 	2.17.12
	@license: 	X11
"""
import bx
import os.path
import sys
import re

#
def BLOX_logo():
	LOGO = (
			'  ____   _     _____  _   ____    _ _____ _ ____  \n'
			' | __ ) | |   / _ \ \/ | |___ \  / |___  / |___ \ \n'
			' |  _ \ | |  | | | \  /    __) | | |  / /| | __) |\n'
			' | |_)  | |__| |_| /  \   / __/ _| | / _ | |/ __/ \n'
			' |____/ |_____\___/_/\_| |_____(_|_|/_(_)|_|_____|'
		)
	bx.color( 'notice', LOGO )
	print( '  UNIVERSAL @BLOX: PREPROCESSOR')

def BLOX_usage():
	print("""
  Usage:
     blox <file:input.bx>
     blox <file:input.bx> <file:output>
     blox <file:input.bx> --@output:<file:output>
     blox <file:input.bx> <flags>
     blox <flags>
     blox --help""")

def BLOX_help():
	print("""
  Flags/Parameters (exampled):
     /? | -h | --help                Show blox help page 
     /l | --@listener                Setting blox to work in listener mode
     --version | /ver                Show blox curretnt version
     --<flag:name>:<flag:value>      Setting <flag:value> to <flag:name>
     --@output:<file:output>         Change output file for interpreter 
     --@echo:off                     Setting @echo to echo off/disabled
     --not-<flag:name>               Setting <flag:name> as disabled
     --<flag:name> | /<flag:name>    Setting <flag:name> as enabled 
     --@debug | /@debug              Setting blox to work in debug mode
     --not-@echo | /not-@echo        Setting @echo to echo off/disabled           

  More:
     More information on official website:
     http://blox.k0ff.eu/""")

def BLOX_exit():
	bx.close()
	try:
		exit()
	except:
		pass	
def BLOX_ver():
	print('BLOX 2.17.12.20171230 @K0FF.EU')

def ARGS():
	args = sys.argv[1:]
	for argument in args:
		match = re.search( r"[/|-]+([\W\w]*)", argument )
		if match:
			argument = match.group(1)
			parameter = argument.lower()

			if parameter in ('h','?','help'):
				PARAMETERS.append('h')
				continue
			
			if parameter in ('v','ver','version'):
				PARAMETERS.append('v')
				continue

			if parameter in ('d'):
				bx.var('@debug',True)
				continue
			
			if parameter in ('w'):
				bx.var('@warnings',True)
				continue

			if parameter in ('l','listener'):
				bx.var('@listener',True)
				continue


			if parameter in ('e','echo','@echo'):
				bx.var('@echo',True)
				continue				

			match = re.search( r"not[-]+([\W\w]*)", argument )
			if match:
				bx.var( match.group(1), False )
				continue

			match = re.search( r"([\W\w]*)\:([\W\w]*)", argument )
			if match:
				bx.var( match.group(1), bx.var._val(match.group(2)) )
				continue

			bx.var( argument, True )
			continue

		else:
			if argument:
				if not bx.var('@input'):
					bx.var('@input',argument)
					continue

				if not bx.var('@output'):
					bx.var('@output',argument)
					continue

				#
				bx.error('Unknown parameter: %s'%(argument))
				BLOX_exit()

			else:
				bx.error('Empty parameter')
				BLOX_exit()

#
bx.PATH = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
	PARAMETERS = []
	bx.reset()
	bx.init()
	bx.load()
	ARGS()
	
	if 'v' in PARAMETERS:
		BLOX_ver()

	if not (PARAMETERS or bx.var('@input')):
		BLOX_logo()
		BLOX_usage()

	#
	if 'h' in PARAMETERS:
		BLOX_logo()
		BLOX_usage()
		BLOX_help()

	#
	if bx.var('@input'):
		OUTPUT = bx.FILE.IMPORT( bx.var('@input') )
		if bx.var('@output'):
			bx.output( OUTPUT )
		bx.status()
