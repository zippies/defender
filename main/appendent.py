# -*- coding: utf-8 -*-
import os,random

class CaseElements(object):
	def __init__(self,element_str):
		self.elementfile = None
		self._parseElement(element_str)

	def _parseXpath(self,xpath):
		eles = []
		if xpath.startswith("//"):
			xpath = xpath[2:]
		xpath_eles = xpath.split("/")
		for ele in xpath_eles:
			if "android.widget." in ele:
				eles.append(ele)
				continue
			else:
				ele = "android.widget.%s" %ele
				eles.append(ele)

		final_xpath = "/".join(eles)

		return "//%s" %final_xpath

	def _parseElement(self,element_str):
		if os.path.exists(element_str):
			with open(element_str,'r') as f:
				self.elementfile = element_str
				element_str = f.read().strip()

		lines = [line for line in element_str.split("\n") if line.strip("\t ")]
		for line in lines:
			try:
				name, by ,value = [s.strip("\t ") for s in line.split('|')]
				if by == 'xpath':
					value = self._parseXpath(value)
				setattr(self,name,(by,value))
			except Exception as e:
				continue

	def get(self,name):
		if hasattr(self,name):
			return getattr(self,name)
		else:
			return (None,None)

class TestData(object):
	def __init__(self,datastr):
		self.testdatafile = datastr
		self._parseDatas(datastr)

	def _parseDatas(self,datastr):
		if os.path.exists(datastr):
			with open(element_str,'r') as f:
				self.datafile = datastr
				datastr = f.read().strip()

		lines = [line for line in datastr.split("\n") if line.strip("\t ")]
		for line in lines:
			try:
				name ,value = [s.strip("\t ") for s in line.split('|')]
				setattr(self,name,eval(value))
			except:
				continue

	def get(self,name,special_index=0):
		if hasattr(self,name):
			values = getattr(self,name)
			if isinstance(values, str):
				return values
			elif isinstance(values, list):
				if special_index > len(values):
					return None
				else:
					return values[special_index-1] if special_index else random.sample(values,1)[0]
		else:
			return None

if __name__ == '__main__':
	from pprint import pprint
	#c = CaseElements('C:\\Users\\Administrator\\Desktop\\selftest\\defender\\elements.txt')
	case_elements = \
	'''
	注册登录按钮		|xpath		 	 |LinearLayout/Button
	手机号输入框		|xpath			 |LinearLayout/RelativeLayout/EditText
	下一步输入密码		|xpath	 		 |RelativeLayout/LinearLayout[2]/ImageView
	密码输入框			|xpath			 |LinearLayout/RelativeLayout/EditText
	登录按钮 			|xpath			 |RelativeLayout/LinearLayout[2]/ImageView
	'''
	c = CaseElements(case_elements)
	pprint(dir(c))
	print(c.get("下一步输入密码"))

# if __name__ == '__main__':
# 	datas = \
# 	'''
# 	usernames	|	[ 11266661001, 11266661002, 11266661003]
# 	passwords	|	[ '111111 ' ]
# 	evaluates 	|	[ "good good study,day day up!" ]
# 	'''
# 	c = TestData(datas)
# 	#pprint(dir(c))
# 	print(c.get("usernames"))
# 	print(c.get("passwords"))
# 	print(c.get("evaluates"))