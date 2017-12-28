#!python
# -*- coding: utf-8 -*-
"""
	@package: 	bx.CODE
	@author: 	KRZYSZTOF "@K0FF.EU" K0FF
	@version: 	2.17.12
"""
import bx

_file = None
_name = None
_line = 0

#
bx._FLAG_SOURCE = False
bx._FLAG_LISTENER = False
bx._FLAG_HALTED = False
bx._FLAG_CODEMODE = False
bx._FLAG_BREAKED = False

#
bx.var('@color.FILE','\033[42;45m')
bx.var('@color.SOURCE','\033[37;43m')
bx.var('@color.BLOCK','\033[42;41m')
bx.var('@color.COMPILE','\033[35;40m')
bx.var('@color.code','\033[37;42m')

#
def listener( text, mode = 'code' ):
	global _line
	message = '%06d|%s'
	if bx._FLAG_COLOR:
		mode = bx.var('@color.'+mode)
		if mode:
			message = mode +'%06d|%s'+ bx.var('@color.reset')
	bx.write( message%( _line, text ) )

#
class Code:

	depth = None
	after = False

	_file = None
	_name = None
	_code = []
	_move = 1

	__iter_begin = 0
	__iter_index = 0
	__iter_before = None
	__iter_stack = []
	__iter_EOL = 0

	def __init__( self, parent = None, **code ):
		if parent:
			self._file = parent._file			
			self._code = parent._code			
			self._move = parent._move			

		if 'name' in code:
			self._name = code['name']

		if 'code' in code:
			self._code = code['code']

		if 'file' in code:
			self._file = code['file']

		if 'begin' in code:
			self.__iter_begin = max( 0, code['begin'] )
		
		if 'EOL' in code:
			self.__iter_EOL = min( code['EOL'], len( self._code ) )
		else:
			self.__iter_EOL = len( self._code )

		if 'move' in code:
			self._move += code['move']

		if 'before' in code:
			self.__iter_before = code['before']

		if 'after' in code:
			self.after = code['after']

	def __iter__( self ):
		self.__iter_stack.append( self.__iter_index )
		self.__iter_index = self.__iter_begin -1
		if self.__iter_before:
			self.__next__ = self.__next_BEFORE;
		else:
			self.__next__ = self.__next_INDEX;
		return self

	def next( self ):
		return self.__next__()

	def __next_BEFORE( self ):
		global _line
		_line = self._move + self.__iter_index
		self.__next__ = self.__next_INDEX;
		return self.__iter_before

	def __next_INDEX( self ):
		global _line
		self.__iter_index += 1
		if self.__iter_index < self.__iter_EOL:
			_line = self._move + self.__iter_index
			return self._code[ self.__iter_index ]
		else:
			self.__iter_index = self.__iter_stack.pop()
			raise StopIteration()

	def __next__( self ):
		raise StopIteration()

	def __source( self, PARSED ):
		global _line
		bx._FLAG_SOURCE = True
		after = PARSED.after
		begin = self.__iter_index +1
		level = 1
		while True:
			self.__iter_index += 1
			if not self.__iter_index < self.__iter_EOL:
				self.__iter_index = self.__iter_EOL -1
				break
			_line = self._move + self.__iter_index
			line = self._code[ self.__iter_index ]

			#
			if bx._FLAG_LISTENER:
				listener( line, 'SOURCE' )

			#
			PARSED = bx.parse( line )
			if not bx.running: break;
			if PARSED.command:
				if PARSED.isBlock:
					level += 1
				elif PARSED.command == 'end':
					level -= 1
					if level == 0:
						break

		if level:
			EOL = self.__iter_index + 1
		else:
			EOL = self.__iter_index

		_line = begin +2
		bx._FLAG_SOURCE = False
		return Code( self,	begin = begin,
							before = after,
							after = PARSED.after,
							EOL = EOL
			)

	def compile( self ):
		bx._FLAG_SOURCE = True
		CODE = []
		BOL = self.__iter_begin
		if self.__iter_before:
			BOL -= 1

		prefix = '#@blox:'
		graber = True
		for line in self:
			if bx._FLAG_LISTENER:
				listener( line, 'COMPILE' )
			line = line.strip()
			if graber:
				if line and not line[0] == ';':
					line = prefix + line
					PARSED = bx.parse( line )
					if not bx.running: break;
					if PARSED.isBlock:
						if PARSED.command in ['echo']:
							graber = False

					CODE.append( line )

				else:
					CODE.append( prefix + ';' + line )

			else:
				if line.lower().find('end') == 0:
					graber = True
					CODE.append( prefix + line )
				else:
					CODE.append( bx.unquote(line.strip()) )
		#
		bx._FLAG_SOURCE = False
		return Code( self,	code = CODE,
							move = BOL,
			)

	def run( self ):
		global _file
		global _name
		global _line

		_prev_file = _file
		_prev_name = _name
		_prev_line = _line

		if self.depth:
			bx.error('Illegal recursion to "%s"'%(self._name))
			return False

		_prev_depth = bx.depth
		bx.depth += 1
		self.depth = bx.depth

		_file = self._file
		_name = self._name

		if bx._FLAG_LISTENER:
			if _file != _prev_file:
				listener( '@%s'%(_file), 'FILE' )
			if _name != _prev_name and _name:
					listener( '#BEGIN:(%s):'%(_name), 'BLOCK' )
			else:
				listener( '#BEGIN:', 'BLOCK' )

		output = ''
		line = ''

		for line in self:
			if bx._FLAG_BREAKED:
				bx._FLAG_BREAKED = False
				break
			if not bx.running: break;
			if bx._FLAG_LISTENER:
				listener( line )
			PARSED = bx.parse( line )
			if not bx.running: break;
			if PARSED.command:

				if PARSED.command in ['end','halt','break']:
					if PARSED.command == 'halt':
						bx._FLAG_HALTED = True
						bx.error('Interpreter halted')
					if PARSED.command == 'break':
						bx._FLAG_BREAKED = True
					if output and output[-1] == '\n':
						output = output[:-1]
					return output

				if PARSED.isBlock:
					SOURCE = self.__source( PARSED )
					result = bx.cmd.execute( PARSED, SOURCE )
					if SOURCE.after:
						if result:
							result += SOURCE.after
						else:
							result = SOURCE.after

				else:
					result = bx.cmd.execute( PARSED )

			else:
				result = PARSED.line

			#
			output += PARSED.result( result )

		if bx._FLAG_LISTENER:
			if _name != _prev_name and _name:
				listener( '#END:(%s);'%(_name), 'BLOCK' )
			else:
				listener( '#END;', 'BLOCK' )
			if _file != _prev_file and _prev_file:
				listener( '#%s'%(_prev_file), 'FILE' )

		_file = _prev_file
		_name = _prev_name

		bx.depth = _prev_depth
		self.depth = None

		if output and output[-1] == '\n':
			return output[:-1]
		if not output:
			return False
		return output

	def listener( self ):
		for line in self:
			print( '%06d|%s'%( bx.CODE._line, line ) )

	def __nonzero__( self ):
		return self.__len__()

	def __len__( self ):
		return self.__iter_EOL - self.__iter_begin

#
def SET_LISTENER( name, value ):
	bx._FLAG_LISTENER = bool( value )
	return bx._FLAG_LISTENER

#
bx.reg.ex('bx.vars.get',{
		'@listener': lambda n: bx._FLAG_LISTENER,
		'@code.file': lambda n: bx.CODE._file,
		'@code.name': lambda n: bx.CODE._name,
		'@code.line': lambda n: bx.CODE._line,
	})

bx.reg.ex('bx.vars.set',{
		'@listener': SET_LISTENER,
		'@code.file': bx.var.readonly,
		'@code.name': bx.var.readonly,
		'@code.line': bx.var.readonly,
	})

#
bx.code = Code