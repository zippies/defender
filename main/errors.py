# -*- coding: utf-8 -*-
class ActionTimeOut(Exception):
	def __init__(self,info):
		self.info = info

	def __str__(self):
		return self.info

class CheckError(Exception):
	def __init__(self,info):
		self.info = info

	def __str__(self):
		return self.info

class CaseError(Exception):
	def __init__(self,info):
		self.info = info

	def __str__(self):
		return self.info

class ConfigError(Exception):
	def __init__(self,info):
		self.info = info

	def __str__(self):
		return self.info