# -*- coding: utf-8 -*-
import os,random

class CaseElements(object):
	def __init__(self,element_str):
		self.elementfile = None
		self._parseElement(element_str)

	def _parseElement(self,element_str):
		if os.path.exists(element_str):
			with open(element_str,'r') as f:
				self.elementfile = element_str
				element_str = f.read().strip()

		lines = [line for line in element_str.split("\n") if line.strip("\t ")]
		for line in lines:
			try:
				name, by ,value = [s.strip("\t ") for s in line.split('|')]
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
	id			|直接登录按钮			|com.wenba.bangbang:id/register_loginTv
	id			|登录用户名输入框			|com.wenba.bangbang:id/login_username_et
	id			|登录密码输入框 	    |com.wenba.bangbang:id/login_passwd_et
	id			|login_btn      	    |com.wenba.bangbang:id/login_login_tv1
	id			|view_history 	        |com.wenba.bangbang:id/skin_home_history_title
	id			|camera        	        |com.wenba.bangbang:id/skin_home_btn_camera
	id			|choose_album   	    |com.wenba.bangbang:id/campage_btn_pic
	id			|all_pics      	        |com.android.documentsui:id/icon_thumb
	id			|submit_pic    	        |com.wenba.bangbang:id/skin_edit_opt_submit
	id			|teacher_answer         |com.wenba.bangbang:id/skin_feed_search_buttom_live_layout
	id			|cancel_red_package     |com.wenba.bangbang:id/btn_cancel
	class_name  |evaluate_teacher  		|android.widget.ImageView
	id			|evaluate_content       |com.wenba.bangbang:id/skin_edt_comment
	id			|evaluate_submit        |com.wenba.bangbang:id/skin_btn_rate_submit
	'''
	c = CaseElements(case_elements)
	pprint(dir(c))
	print(c.get("直接登录按钮"))

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