# -*- coding: utf-8 -*-
from main.android.basecase import AndroidDevice

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
		self.casename = '%s_%s_%s' %(dc['deviceName'],ce['port'],self.filename)

	def __call__(self,conflict_datas):
		super(TestCase,self).__init__(conflict_datas,command_executor=self.appium_url,desired_capabilities=self.dc)
		return self

	# 需要修改
	def run(self):
		#设置隐式等待为10秒
		self.implicitly_wait(10)
		#允许使用摄像头
		self.allow_alert()
		#不注册点击登录
		self.super_click('直接登录按钮')
		#拿到与其他设备不相冲突的账号
		username,password = self.get_conflict('登录帐号')
		#输入账号
		self.super_input('登录用户名输入框',username)
		#输入密码
		self.super_input('登录密码输入框',password)
		#点击登录按钮
		self.super_click('登录按钮')
		#等待2秒
		self.sleep(2)
		#截图
		self.save_screen('login')
		#点击拍照搜题
		self.super_click('拍照搜题按钮')
		#允许调用摄像头
		self.allow_alert()
		self.save_screen('camera')
		#点击相册
		self.super_click('相册')
		#找到相册内所有图片  选择第一张点击
		self.save_screen()
		eles = self.super_finds('所有图片')[1].click()
		self.save_screen()
		#点击提交按钮
		self.super_click('提交图片')
		self.save_screen()
		#点击老师答疑
		self.super_click('老师答疑')
		self.save_screen()
		#同意调用录音
		self.allow_alert(nocheck=True)
		#等直到出现取消发红包按钮 并点击
		btn = self.super_waitfor('取消分享红包',timeout=120).click()
		#评星级	五星
		ele = self.super_finds('所有评价星星')[4].click()
		#点评内容 输入"good good study day day up"
		content = self.test_datas.get('评价内容')
		self.super_input('评价输入框',content)
		#提交点评
		self.super_click('提交评价')
