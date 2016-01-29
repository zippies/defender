# -*- coding: utf-8 -*-
from main.android.basecase import AndroidDevice
from xml.dom import minidom
from pprint import pprint

class TestCase(AndroidDevice):
	# 需要修改  desc：描述这个测试脚本测试的内容
	desc = "答疑流程是否正常"

	def __init__(self,ce,dc):
		self.dc = dc
		self.appium_port = ce['port']
		self.bootstrap_port = ce['bootstrap_port']
		self.device_name = dc['deviceName']
		self.appium_url = ce['url']
		self.filename = str(self.__class__).split('.')[0].split('\'')[1]
		self.casename = '%s_%s_%s' %(dc['deviceName'].replace('.','_').replace(":","_"),ce['port'],self.filename)

	def __call__(self,conflict_datas):
		super(TestCase,self).__init__(conflict_datas,command_executor=self.appium_url,desired_capabilities=self.dc)
		return self

	# 需要修改
	def run(self):
		#设置隐式等待为10秒
		self.implicitly_wait(10)
		#允许使用摄像头
		#self.super_click("跳过")
		ele = self.find('id','com.xinjing.jingfree:id/tabHost')
		eles = ele.find_elements_by_class_name('android.widget.RelativeLayout')
		for e in eles:
			print(e.find_elements_by_class_name('android.widget.TextView')[1].text)