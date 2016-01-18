# -*- coding: utf-8 -*-
import logging,os
from threading import Thread

class Logger(object):
	def __init__(self,name,mode):
		self.mode = mode
		self.format = '[%(levelname)s] %(asctime)s %(message)s'
		fm = logging.Formatter(self.format) 
		logging.basicConfig(
				level = logging.DEBUG,
				format = self.format,
				datefmt = '%Y_%m_%d %H:%M:%S',
				filename = 'tmp',
				filemode = 'w'
		)
		
		infohandler = logging.FileHandler('%s_info.log' %name)
		infohandler.setLevel(logging.INFO)
		infohandler.setFormatter(fm)
		self.infologger = logging.getLogger('%sinfologger' %name)
		self.infologger.addHandler(infohandler)

	def log(self,msg):
		if self.mode == 'null':
			return
		elif self.mode == 'print':
			print(msg)
		else:
			if self.mode == 'file':
				self.infologger.info(msg)
			else:
				self.infologger.info(msg)
				print(msg)
