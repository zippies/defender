#coding:utf-8
import sys,os,time,requests
from configs.androidConfig import casepath,\
									logpath,\
									snapshotpath,\
									case_logmode,\
									appium_log_level,\
									devices,\
									shared_capabilities
sys.path.append(casepath)
sys.path.append("main")
from android.logger import Logger
from threading import Thread
from datetime import datetime
from pprint import pprint

class AndroidRunner(object):
	def __init__(self):
		self.casefiles = [file[:-3] for file in os.listdir(casepath) if file.endswith('.py')]
		self.current_time = time.time()
		self.logtime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		self.static_forder = os.path.abspath('static')
		self.devices = devices
		self.appiums = self._initAppium()
		self.logdir = os.path.join(logpath,self.logtime)
		self.testcases = {}
		self.result = {
				"success":[],
				"failed":[],
				"casecount":0,
				"duration":0,
				"report":None
		}
		self._initdir('log')
		self._initcase()
		self._initdir('screenshot')
		
	def _initAppium(self):
		'''
			从配置初始化设备和appium服务信息
		'''
		appiums = []
		for index,device in enumerate(self.devices):
			for key,value in shared_capabilities.items():
				device[key] = value
			self.devices[index] = device
			port = str(14230 + index)
			appiums.append({"port":port,"url":"http://localhost:%s/wd/hub" %port})

		return appiums

	def _initdir(self,type):
		'''
			初始化(如果不存在则创建)日志文件夹路径和截图文件夹路径
		'''
		if type == "log" and case_logmode not in ['print','null']:
			os.makedirs(self.logdir)

		elif type=="screenshot":
			for cases in self.testcases.values():
				for case in cases:
					case_screenshot = os.path.join(snapshotpath,case.casename,self.logtime)
					os.makedirs(case_screenshot)
					setattr(case,'screenshotdir',case_screenshot)
		else:
			pass

	def _initcase(self):
		'''
			初始化测试用例
		'''
		for case in self.casefiles:
			t_case = []
			for index,device in enumerate(self.devices):
				t_case.append(__import__(case).TestCase(self.appiums[index],device))
				self.result['casecount'] += 1
			self.testcases[case] = t_case

	def checkSystemStat():
		'''
			检查当前系统端口占用情况和设备连接情况
		'''
		pass

	def startAppium(self,cases,timeout=20):
		'''
			每个连接的设备(手机)对应启动一个appium服务
		'''
		appium_thread_list = []
		for case in cases:
			appiumlog = os.path.join(self.logdir,case.device_name + "_" + case.appium_port + "_appium.log")
			cmd = "D:/Appium/node_modules/.bin/appium\
					 -a 127.0.0.1 \
					 -p %s \
					 -g %s \
					 --log-timestamp \
					 --log-level %s \
					 -U %s \
					 --log-no-colors" %(case.appium_port,appiumlog,appium_log_level,case.device_name)
			t = Thread(target=os.system,args=(cmd,))
			t.daemon = True
			appium_thread_list.append(t)

		for t in appium_thread_list:
			t.start()

		for case in cases:
			starts = time.time()
			while time.time() - starts < timeout:
				try:
					r = requests.get('http://localhost:%s/wd/hub' %case.appium_port)
					if r.status_code == 404:
						print("[success]Appium started on port : %s ! %s" %(case.appium_port,case.device_name))
						break
					else:
						time.sleep(0.5)
				except:
					continue
			else:
				print("[failure]Start Appium failed on port: %s !" %case.appium_port)
				sys.exit(-1)

	def stopAppium(self):
		'''
			关闭所有appium服务
		'''
		os.system("taskkill /F /IM node.exe")
				
	def runMultiTest(self):
		'''
			运行所有测试用例
		'''

		for cases in self.testcases.values():
			self.startAppium(cases)
			time.sleep(20)
			testjobs = []
			for case in cases:
				caselog = os.path.join(self.logdir,case.casename+"_case")
				logger = Logger(caselog,case_logmode)
				setattr(case,'logger',logger)
				setattr(case, 'result', {"errorMsg":None})
				setattr(case, 'appiumlogfile', os.path.join(self.logdir,case.device_name+"_"+case.appium_port+"_appium.log"))
				setattr(case,'caselogfile',caselog+"_info.log")
				c = case()
				
				t = Thread(target=self.runTest,args=(c,))
				testjobs.append(t)

			for job in testjobs:
				job.start()

			for job in testjobs:
				job.join()

			self.stopAppium()

	def runTest(self,case):
		start = time.time()
		try:
			print("running test:",case.casename)
			case.run()
		except Exception as e:
			print(e)
			case.save_screen("Error_"+case.casename)
			case.result['result'] = False
			case.result['errorMsg'] = str(e)
			self.result['failed'].append(case)
		finally:
			end = time.time()
			case.result['runtime'] = round(end-start,2)
			case.close_app()
			case.quit()

		if 'result' not in case.result.keys():
			case.result['result'] = True
			self.result['success'].append(case)


	def getReportContext(self):
		try:
			with open('main/report_template.html','r',encoding='utf-8') as f:
				return f.read()
		except Exception as e:
			return ""

	def processCase(self,result):
		for case in result['success'] + result['failed']:
			with open(case.appiumlogfile,'r') as f:
				setattr(case,'appiumlogcontent',f.readlines())
			with open(case.caselogfile,'r') as f:
				setattr(case,'caselogcontent',f.readlines())

			setattr(case,'screenshotimgs',[[file,os.path.join(case.screenshotdir,file)] for file in os.listdir(case.screenshotdir)])

	def generateReport(self):
		from jinja2 import Template
		context = self.getReportContext()

		self.processCase(self.result)

		html = Template(context).render(
								result=self.result,
								device_count=len(self.devices),
								casecount=len(self.casefiles),
								totalcount=self.result['casecount'],
								success=len(self.result['success']),
								failed=len(self.result['failed']),
								static_forder=self.static_forder
								)
		report = os.path.join(self.logdir,'report.html')
		with open(report,'w',encoding='utf-8') as f:
			f.write(html)

		self.result['duration'] = round(time.time() - self.current_time,2)
		self.result['report'] = report

		pprint(self.result)

if __name__ == '__main__':
	runner = AndroidRunner()
	runner.runMultiTest()
	runner.generateReport()
	#如果命令行参数大于1个,用默认浏览器打开测试报告 python androidRunner.py type_anything_here
	if len(sys.argv) > 1:
		os.system('start %s' %runner.result['report'])