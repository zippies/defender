# -*- coding: utf-8 -*-
#用例日志模式:file(日志写文件,不在终端打印)|print(日志在终端打印,不写文件)|all(日志既在终端打印,同时写文件)
case_logmode = "file"

#appium的日志级别：
#info, info:debug, info:info, info:warn, info:error, warn, warn:debug, warn:info, warn:warn, warn:error, error, error:debug, error:info, error:warn, error:error, debug, debug:debug, debug:info, debug:warn, debug:error
appium_log_level = "error"

#测试用例存放目录
casepath = "C:\\Users\\Administrator\\Desktop\\selftest\\defender\\testcases"

#日志/测试报告 存放目录
logpath = "C:\\Users\\Administrator\\Desktop\\selftest\\defender\\logs"

#截图文件存放目录
snapshotpath = "C:\\Users\\Administrator\\Desktop\\selftest\\defender\\snapshots"

#电脑连接上的设备(有多台则写多台)
devices = [
	# {
	# 	"deviceName":"192.168.56.101:5555", #"虚拟机"
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# }
	# {
	# 	"deviceName":"10.88.1.223:5555", #"9L5T99MNPZDEW4I7", #lenovo
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# },
	# {
	# 	"deviceName":"81CEBMJ22YEC", #MEIZU PRO 81CEBMJ22YEC
	# 	"platformName":"Android",
	# 	"platformVersion":"5.1"
	# },
	# {
	# 	"deviceName":"10.88.0.86:5555", #MEIZU 3X
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# }
	# {
	# 	"deviceName":"10.88.1.221:5555", #green MEIZU  71CDBLL233YA
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# }
	{
		"deviceName":"M3LDU15424001636",  #honor 6
		"platformName":"Android",
		"platformVersion":"4.4"
	}
]

#所有设备共享的与appium的连接参数
#需要的参数可在appium官网查看用途：http://appium.io/slate/en/master/?python#appium-server-capabilities
shared_capabilities = {
	"app" : "C:\\Users\\Administrator\\Downloads\\apks\\backup.apk",	#也可在命令行指定apk
	"appPackage" : "com.wenba.bangbang",
	"appActivity" : "com.wenba.bangbang.activity.CoverActivity",
	"newCommandTimeout" : 120,
	"noSign" : True,
	"unicodeKeyboard":True,
	"resetKeyboard":True
}

# shared_capabilities = {
# 	#"app" : "C:\\Users\\Administrator\\Downloads\\apks\\jingfree.apk",	#也可在命令行指定apk
# 	"appPackage" : "com.xinjing.jingfree", #"com.wenba.bangbang",
# 	"appActivity" : "com.xinjing.jingfree.MainActivity_",#"com.wenba.bangbang.activity.CoverActivity",
# 	"newCommandTimeout" : 120,
# 	"noSign" : True,
# 	"unicodeKeyboard":True,
# 	"resetKeyboard":True
# }

#系统权限弹框中允许/拒绝按钮的id
system_alert_ids = [
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
注册登录按钮		|xpath		 	 |LinearLayout/Button
手机号输入框		|xpath			 |LinearLayout/RelativeLayout/EditText
下一步输入密码		|xpath	 		 |RelativeLayout/LinearLayout[2]/ImageView
密码输入框			|xpath			 |LinearLayout/RelativeLayout/EditText
登录按钮 			|xpath			 |RelativeLayout/LinearLayout[2]/ImageView
查看历史按钮		|id			 	 |com.wenba.bangbang:id/skin_home_history_title
未提问图片			|id 		 	 |com.wenba.bangbang:id/beat_loading_img
拍照搜题按钮		|xpath			 |RelativeLayout/FrameLayout/FrameLayout/ImageView
相册				|id				 |com.wenba.bangbang:id/campage_btn_pic
不兼容相册列表		|id 			 |com.meizu.documentsui:id/menu_frame
不兼容的所有图片	|id	 			 |android:id/text1
所有图片			|id 			 |com.android.documentsui:id/icon_thumb
提交图片			|id				 |com.wenba.bangbang:id/skin_edit_opt_submit
老师答疑			|id				 |com.wenba.bangbang:id/skin_feed_search_buttom_live_layout
取消分享红包		|id				 |com.wenba.bangbang:id/btn_cancel
所有评价星星		|class_name 	 |android.widget.ImageView
优先选择该老师答疑	|id 			 |com.wenba.bangbang:id/skin_teacher_preference_checkbox
评价输入框			|id	    		 |com.wenba.bangbang:id/skin_edt_comment
提交评价			|id		   		 |com.wenba.bangbang:id/skin_btn_rate_submit

跳过				|id 			 |com.xinjing.jingfree:id/tvJump
搜索				|id 			 |com.xinjing.jingfree:id/imgLeft
所有热门商品		|id 			 |com.xinjing.jingfree:id/tvKeyName
价格信息			|id 			 |com.xinjing.jingfree:id/ptvPrice
'''

# case_elements = \
# '''
# 跳过				|id 		 |com.xinjing.jingfree:id/tvJump
# 镜福利				|id 		 |android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.support.v4.view.ViewPager/android.widget.RelativeLayout/android.view.View/android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ImageView
# 搜索				|id 		 |com.xinjing.jingfree:id/imgLeft
# 所有热门商品		|id 		 |com.xinjing.jingfree:id/tvKeyName
# 价格信息			|id 		 |com.xinjing.jingfree:id/ptvPrice
# '''

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