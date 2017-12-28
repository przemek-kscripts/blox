#!python
# -*- coding: utf-8 -*-
"""
	@package:	cmd.@time
	@author:	KRZYSZTOF "@K0FF.EU" K0FF
	@version:	2.17.12
"""
import bx
import time

#
LOCALTIME = time.localtime()

#
def TIME( name ):
	global LOCALTIME
	if name == '#time':
		H = LOCALTIME.tm_hour
		M = LOCALTIME.tm_min
		d = M%5
		if d:
			d += float(LOCALTIME.tm_sec)/60
			M += 5-int(d) if d > 2.5 else -int(d)
			if M > 59:
				M = 0
				H += 1
				if H > 23: H = 0
		return '%02d:%02d'%(H,M)

	elif name == '#time.now':
		return time.strftime("%H:%M:%S", time.localtime())

	elif name == '#date.now':
		return time.strftime("%Y-%m-%d", time.localtime())


#
bx.reg.ex('bx.vars',{
		'#date': time.strftime("%Y-%m-%d", LOCALTIME),
		'#time': TIME('#time')
	})

#
bx.reg.ex('bx.vars.set',{
		'#time.now': bx.var.readonly,
		'#date.now': bx.var.readonly,
	})

bx.reg.ex('bx.vars.get',{
		'#time.now': TIME,
		'#date.now': TIME,
	})
