#用例日志模式:file|print|all
#file:日志写文件,不在终端打印
#print:日志在终端打印,不写文件
#all:日志即在终端打印,同时写文件
case_logmode = "file"

#appium的日志级别：debug|info|error
appium_log_level = "info"

#测试用例存放目录
casepath = "C:\\Users\\Administrator\\Desktop\\defender\\testcases"

#日志/测试报告 存放目录
logpath = "C:\\Users\\Administrator\\Desktop\\defender\\logs"

#截图文件存放目录
snapshotpath = "C:\\Users\\Administrator\\Desktop\\defender\\snapshots"

#电脑连接上的设备(有多台则写多台)
devices = [
	{
		"deviceName":"351ABHDPKBLX",  #MX3
		"platformName":"Android",
		"platformVersion":"4.4"
	}#,
	# {
	# 	"deviceName":"9L5T99MNPZDEW4I7", #lenovo
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# }
	# {
	# 	"deviceName":"M3LDU15424001636",  #honor 6
	# 	"platformName":"Android",
	# 	"platformVersion":"4.4"
	# }
]

#所有设备共享的与appium的连接参数
#需要的参数可在appium官网查看用途：http://appium.io/slate/en/master/?ruby#appium-server-capabilities
shared_capabilities = {
	"app" : "C:\\Users\\Administrator\\Downloads\\wenba_xbj_v4.6.1_qa_server.apk",
	"appPackage" : "com.wenba.bangbang",
	"appActivity" : "com.wenba.bangbang.activity.CoverActivity",
	"newCommandTimeout" : 120,
	"noSign" : True
}
