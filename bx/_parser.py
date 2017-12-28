#!python
# -*- coding: utf-8 -*-
"""
	@package:	bx._parser
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import re

#
_REXP = r'(%s)[\s]*@blox:'%('|'.join([
			r'#[#\s]*',
			r'//[/\s]*',
			r'<!--[-\s]*',
			r'::[:\s]*',
			r'/\*[\*\s]*',
			r'"""["\s]*',
			r'%[%\s]*',
	]))

#
class Parsed:
	command = False
	arguments = False
	after = False
	before = False
	isBlock = False
	alias = False
	length = 0
	line = ''

	def __init__( self, line ):
		self.line = line = bx.var.filter( line )
		match = re.search( _REXP, line, re.IGNORECASE )

		if match:
			self.before = line[ 0: match.start() ]
			line = line[ match.end(): ]
			mode = self.__mode( match )

			#
			if mode == '/' or mode == '*':
				line = self.__after( line, '*/', ' *' )

			if mode == '<':
				line = self.__after( line, '-->', ' -' )

			if mode == '#' or mode == '"':
				line = self.__after( line, '"""' ) 

			#
			command = self.__command( line )

			#
			command[0] = command[0].lower()
			self.command = bx.cmd.isCommand( command[0] )
			if self.command != command[0]:
				self.alias = command[0]
			if len(command)>1:
				self.arguments = command[1:]
				self.length = len(self.arguments)
			if self.command:
				self.isBlock = bx.cmd.isBlock( self )

			if self.after and re.search( _REXP, self.after.lower() ):
				bx.error('Multiple blox command')
				return None

	@staticmethod
	def __mode( match ):
		if match.group(0)[0] == '"': return '"'
		if match.group(0)[0] == '#': return '#'
		if match.group(0)[0] == '<': return '<'
		if match.group(0)[0] == ':': return ':'
		if match.group(0)[0] == '%': return '%'		
		if match.group(0)[1] == '/': return '/'
		if match.group(0)[1] == '*': return '*'	

	@staticmethod
	def __command( command ):
		command = command.strip()
		if command[0] == ';':
			return [';']
			
		result = []
		splits = command.split(':')
		factor = ''
		
		for split in splits:
			if factor:
				factor += ':' + split
			else:
				factor = split

			C = factor.lstrip()
			if len(C) and C[0] == '"':
				A = C.rfind('"')
				B = factor.rfind(';')

				if A > 0 and A < B:
					factor = factor[:B]

				if factor.rstrip()[-1] == '"':
					result.append( factor.strip() )
					factor = ''
				
				continue

			B = factor.find(';')
			if B > -1:
				factor = factor[:B]

			result.append( factor.strip() )
			factor = ''			

		result.reverse()
		splits = result
		eraser = True
		result = []
		for split in splits:
			if not split and eraser:
				continue
			else:
				split = bx.unquote( split )
				eraser = False
				result.append( split )
		
		if len(splits)-1 > len(result):
			bx.warning('Many Empty parameters')
			pass
		result.reverse()

		if len(result):
			if result[0]:
				result[0] = result[0].lower()
			else:
				bx.warning('Empty command')
				return [';']
		else:
			return [';']
		return result	

	def __after( self, line, end = None, stripper = None ):
		if end:
			find = line.find( end )
			if not find == -1:
				self.after = line[ find + len(end): ]
				line = line[ :find ]
				if stripper:
					line = line.rstrip( stripper )
		return line

	def __nonzero__( self ):
		return bool( self.command )

	def result( self, result = False ):
		output = ''
		if self.command and self.before:
			output = self.before
		if result:
			output += result
		if bx.running:
			if not self.isBlock and self.after:
				output += self.after
			if result or not self.command or self.after:
				output += '\n'
		return output

#
bx.parse = Parsed