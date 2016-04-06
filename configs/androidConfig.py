# -*- coding: utf-8 -*-
#用例日志模式:file(日志写文件,不在终端打印)|print(日志在终端打印,不写文件)|all(日志既在终端打印,同时写文件)
case_logmode = "file"

#appium的日志级别：
#info, info:debug, info:info, info:warn, info:error, warn, warn:debug, warn:info, warn:warn, warn:error, error, error:debug, error:info, error:warn, error:error, debug, debug:debug, debug:info, debug:warn, debug:error
appium_log_level = "info"

#测试用例存放目录
casepath = "C:\\Users\\Lin\\Desktop\\selftest\\defender\\testcases"

#日志/测试报告 存放目录
logpath = "C:\\Users\\Lin\\Desktop\\selftest\\defender\\logs"

#截图文件存放目录
snapshotpath = "C:\\Users\\Lin\\Desktop\\selftest\\defender\\snapshots"

#电脑连接上的设备(有多台则写多台)
devices = [
	# {
	# 	"deviceName":"192.168.56.101:5555", #"虚拟机"
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# },
	# {
	# 	"deviceName":"192.168.199.149:5555", #MEIZU x2
	# 	"platformName":"Android",
	# 	"platformVersion":"5.1"
	# },
	{
		"deviceName":"NHG6T15C26001819", #huawei
		"platformName":"Android",
		"platformVersion":"5.1"
	},
	# {
	# 	"deviceName":"d1b24e2f", #vivo  
	# 	"platformName":"Android",
	# 	"platformVersion":"5.0"
	# },
	{
		"deviceName":"M3LDU15424001636",  #honor 6
		"platformName":"Android",
		"platformVersion":"4.4"
	}
]

#所有设备共享的与appium的连接参数
#需要的参数可在appium官网查看用途：http://appium.io/slate/en/master/?python#appium-server-capabilities
shared_capabilities = {
	#"app" : "C:\\Users\\Lin\\Desktop\\undertest\\app-release.apk",	#也可在命令行指定apk
	"appPackage" : "me.sui.arizona",
	"appActivity" : "me.sui.arizona.ui.activity.FirstPageActivity",
	"newCommandTimeout" : 120,
	"noSign" : True,
	"unicodeKeyboard":True,
	"resetKeyboard":True
}

#系统权限弹框中允许/拒绝按钮的id
system_alert_ids = [
	('me.sui.arizona:id/btn_right','me.sui.arizona:id/btn_left'),
	('com.huawei.systemmanager:id/btn_allow','com.huawei.systemmanager:id/btn_forbbid'),
	('android:id/button1','android:id/button'),
	('flyme:id/accept','flyme:id/reject')
]

#需要在case内用到的所有元素(实现元素和case分离)
#数据格式----以两个'|'符号分隔开的三块内容分别代表：元素名称 | 元素定位方式(id/class_name/name/..同selenium) | 定位方式使用的值
#case内用法：
#	self.super_click('直接登录按钮')    #super_click(name) 该方法是框架内定义的方法，更多用法参见main/android/basecase.py
case_elements = \
'''
注册按钮		|id		 	 |me.sui.arizona:id/btn_login
'''

#需要在case内用到的测试数据(实现测试数据和case分离)
#数据格式----以'|'符号分隔的name和value：	name  |   value
#case内用法：
#	comments = self.test_datas.get('评价内容')	#随机返回一个'评价内容'列表内的值
#	comments = self.test_datas.get('评价内容',1)   #指定获取第1条数据("good good study,day day up! ")
#	data = self.test_datas.get('测试数据')   #获取"abcdef123456"
test_datas = \
'''
评价内容 	|	[ "好好学习,天天向上!   " , "你行你上，不行别BB   " ]
测试数据	|	"abcdef123456"
'''

#适用场景：在相同case运行在多个终端时，每个终端通过相同的name调用方法self.get_conflict(name)能获取到不同数据
#该配置解决在多个设备同时跑相同case的场景下可能存在的数据冲突
#例如：两个手机同时跑登录的case，如果case内使用帐号相同则会存在帐号冲突，导致某一台手机case运行失败
#数据格式----以'|'符号分隔的name和value(list类型)：	name  |   value
#用法：
#	username,password = self.get_conflict('登录帐号')
#	other_data = self.get_conflick('其他数据')
#[注意]：
#	在case内有使用的name，其value内配置的值个数不能少于使用的设备数！
conflict_datas = \
'''
登录帐号	|	[ ('11266661001','111111'), ('11266661002','111111'), ('11266661004','111111'),('11266661005','111111'),('11266661007','111111'),('11266661008','111111')]
其他数据	|	[1,2]
'''