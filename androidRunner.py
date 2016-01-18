# -*- coding: utf-8 -*-
import sys,os,time,requests,platform
from configs.androidConfig import casepath,\
									logpath,\
									snapshotpath,\
									case_logmode,\
									appium_log_level,\
									devices,\
									system_alert_ids,\
									shared_capabilities,\
									case_elements,\
									test_datas,\
									conflict_datas
sys.path.append(casepath)
from main import Logger,TestData,CaseElements,ConfigError
from multiprocessing import Process
from threading import Thread
from datetime import datetime
from pprint import pprint

class AndroidRunner(object):
	def __init__(self,singlecase=None,test_devices=None,apk_file=None):
		self.apk_file = apk_file or shared_capabilities.get('app')
		self.singlecase = singlecase
		self.devices = devices if not test_devices else [test_devices]
		self.reachable_devices = None
		self._connectWirelessDevices()
		self._checkConfig()
		self.current_system = platform.system()
		self.case_elements = CaseElements(case_elements)
		self.test_datas = TestData(test_datas)
		self.current_time = time.time()
		self.logtime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		self.static_forder = os.path.abspath('static')
		self.appiums = self._initAppium()
		self.logdir = os.path.join(logpath,self.logtime)
		self.testcases = {}
		self.result = {
				"success":[],
				"failed":[],
				"totalcount":0,
				"casecount":0,
				"duration":0,
				"report":None
		}
		self._initcase(singlecase)
		self._initdirs()

	def _connectWirelessDevices(self):
		from subprocess import Popen,PIPE
		import re
		cmd = 'adb devices'
		p = Popen(cmd,stdout=PIPE,shell=True)
		reachable_devices = [info.decode().split('device')[0].strip('\t ') for info in p.stdout.readlines() if info.decode().strip('\r\n')][1:]
		pattern = re.compile("([0-9]{1,3}.){3}[0-9]{1,3}:[0-9]{4}")
		for device in self.devices:
			match = pattern.match(device['deviceName'])
			if match and device['deviceName'] not in reachable_devices:
				result = os.system("adb connect %s" %device['deviceName'])
				if result != 0:
					print(device['deviceName'],result)
					raise ConfigError("device:%s is not reachable currently111" %device['deviceName'])

		time.sleep(1)	#等待授权
		pp = Popen(cmd,stdout=PIPE,shell=True)
		self.reachable_devices = [info.decode().split('device')[0].strip('\t ') for info in pp.stdout.readlines() if info.decode().strip('\r\n')][1:]

	def _checkConfig(self):
		if case_logmode not in ['print','file','all']:
			raise ConfigError("no such case_logmode '%s' ,it should be one of [ file| print| all]" %case_logmode)

		if appium_log_level not in ['info', 'info:debug', 'info:info', 'info:warn', 'info:error', 'warn', 'warn:debug', 'warn:info', 'warn:warn', 'warn:error', 'error', 'error:debug', 'error:info', 'error:warn', 'error:error', 'debug', 'debug:debug', 'debug:info', 'debug:warn', 'debug:error']:
			raise ConfigError("no such appium_log_level '%s' ,it should be one of [ info, info:debug, info:info, info:warn, info:error, warn, warn:debug, warn:info, warn:warn, warn:error, error, error:debug, error:info, error:warn, error:error, debug, debug:debug, debug:info, debug:warn, debug:error]" %appium_log_level)

		if len([case for case in os.listdir(casepath) if case.endswith('.py')]) == 0:
			raise ConfigError("no case file found in '%s'" %casepath)

		if self.apk_file:
			if not os.path.exists(self.apk_file):
				raise ConfigError("file not found:%s" %self.apk_file)

		config_devices = [device['deviceName'] for device in self.devices]
		for device in config_devices:
			if device not in self.reachable_devices:
				raise ConfigError("device:%s is not reachable currently" %device)

	def _parseConflictData(self,datastr):
		datas = {}
		if os.path.exists(datastr):
			with open(datastr,'r') as f:
				datastr = f.read().strip()

		lines = datastr.split("\n")
		for line in lines:
			try:
				name ,value = [s.strip("\t ") for s in line.split('|')]
				datas[name] = eval(value)
			except:
				continue
		return datas

	def _initAppium(self):
		'''
			从配置初始化设备和appium服务信息
		'''
		appiums = []
		for index,device in enumerate(self.devices):
			for key,value in shared_capabilities.items():
				device[key] = value
			if self.apk_file:
				device["app"] = self.apk_file
			device['automationName'] = 'Appium' if float(device['platformVersion']) > 4.2 else 'Selendroid'
			self.devices[index] = device
			port = str(13230 + index)
			bootstrap_port = str(14230 + index)
			selendroid_port = str(15230 + index)
			appiums.append({"port":port,"bootstrap_port":bootstrap_port,"url":"http://localhost:%s/wd/hub" %port})

		return appiums

	def _initdirs(self):
		'''
			初始化(如果不存在则创建)日志文件夹路径和截图文件夹路径
		'''
		if case_logmode not in ['print','null']:
			os.makedirs(self.logdir)

		for cases in self.testcases.values():
			for case in cases:
				case_screenshot = os.path.join(snapshotpath,case.casename,self.logtime)
				os.makedirs(case_screenshot)
				setattr(case,'screenshotdir',case_screenshot)

	def _initcase(self,singlecase):
		'''
			初始化测试用例
		'''
		casefiles = [singlecase] if singlecase else [file[:-3] for file in os.listdir(casepath) if file.endswith('.py')]
		casefiles.reverse()
		self.result['casecount'] = len(casefiles)
		for case in casefiles:
			t_case = []
			for index,device in enumerate(self.devices):
				t_case.append(__import__(case).TestCase(self.appiums[index],device))
				self.result['totalcount'] += 1
			self.testcases[case] = t_case

	def is_Appium_Alive(self,port):
		'''
			检查指定端口的appium是否已启动
		'''
		try:
			r = requests.get('http://localhost:%s/wd/hub' %port)
			if r.status_code == 404:
				return True
			else:
				return False
		except Exception as e:
			return False

	def startAppium(self,cases,timeout=30):
		'''
			每个连接的设备(手机)对应启动一个appium服务
		'''
		appium_process_list = []
		for case in cases:
			appiumlog = os.path.join(self.logdir,case.device_name + "_" + case.appium_port + case.filename + "_appium.log")
			cmd = "appium\
					 -a 127.0.0.1 \
					 -p %s \
					 -bp %s \
					 -g %s \
					 --log-timestamp \
					 --log-level %s \
					 -U %s \
					 --log-no-colors" %(case.appium_port,case.bootstrap_port,appiumlog,appium_log_level,case.device_name)
			p = Process(target=os.system,args=(cmd,))
			p.daemon = True
			appium_process_list.append(p)
			if self.is_Appium_Alive(case.appium_port):
				self.stopAppium()
			print("[action]Starting Appium on port : %s bootstrap_port: %s for device %s" %(case.appium_port,case.bootstrap_port,case.device_name))

		for p in appium_process_list:
			p.start()

		for case in cases:
			starts = time.time()
			while time.time() - starts < timeout:
				if self.is_Appium_Alive(case.appium_port):
					print("[success]Appium started on port : %s bootstrap_port: %s for device %s" %(case.appium_port,case.bootstrap_port,case.device_name))
					break
				else:
					time.sleep(0.5)
			else:
				print("[failure]Start Appium failed on port: %s bootstrap_port: %s for device %s!" %(case.appium_port,case.bootstrap_port,case.device_name))
				self.stopAppium()
				sys.exit(-1)

	def stopAppium(self):
		'''
			关闭所有appium服务
		'''
		if self.current_system == 'Windows':
			os.system("taskkill /F /IM node.exe")
		else:
			os.system("killall node")

	def runMultiTest(self):
		'''
			运行所有测试用例
		'''
		try:
			for cases in self.testcases.values():
				self.startAppium(cases)
				testjobs = []
				datas = self._parseConflictData(conflict_datas)
				for case in cases:					
					t = Thread(target=self.runTest,args=(case,datas))
					testjobs.append(t)

				for job in testjobs:
					job.start()

				for job in testjobs:
					job.join()
		except Exception as e:
			print("error occured while running 'runMultiTest':",str(e))
		finally:
			time.sleep(2)
			self.stopAppium()

	def runTest(self,case,datas):
		print("[action]Initializing case %s" %case.casename)
		start = time.time()
		initsuccess = False
		caselog = os.path.join(self.logdir,case.casename+"_case")
		logger = Logger(caselog,case_logmode)
		setattr(case,'logger',logger)
		setattr(case, 'result', {"errorMsg":None})
		setattr(case, 'appiumlogfile', os.path.join(self.logdir,case.device_name+"_"+case.appium_port+case.filename+"_appium.log"))
		setattr(case,'caselogfile',caselog+"_info.log")
		setattr(case,'case_elements',self.case_elements)
		setattr(case,'test_datas',self.test_datas)
		setattr(case,'system_alert_ids',system_alert_ids)
		try:
			case = case(datas)
			initsuccess = True
			print("[action]running test:%s %s" %(case.casename,case.desc))
			case.run()
		except Exception as e:
			errorMsg = str(e)
			case.logger.log("[ERROR]%s" %errorMsg)
			if initsuccess:
				case.save_screen("error",immediate=True)
			case.result['result'] = False
			case.result['errorMsg'] = errorMsg
			self.result['failed'].append(case)
		finally:
			end = time.time()
			case.result['runtime'] = round(end-start,2)
			print("end test:",case.casename)
			if initsuccess:
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
			if os.path.exists(case.appiumlogfile):
				with open(case.appiumlogfile,'r') as f:
					setattr(case,'appiumlogcontent',f.readlines())
			else:
				setattr(case,'appiumlogcontent',['appium log did not generated,check "androidConfig.py" whether "appium_log_level" has been set to "error",try "info" or "debug" instead'])
			if os.path.exists(case.caselogfile):
				with open(case.caselogfile,'r') as f:
					setattr(case,'caselogcontent',f.readlines())
			else:
				setattr(case,'caselogcontent',['no case action recorded'])

			setattr(case,'screenshotimgs',[[file,os.path.join(case.screenshotdir,file)] for file in os.listdir(case.screenshotdir)])

	def generateReport(self,report_path=None):
		from jinja2 import Template
		context = self.getReportContext()

		self.processCase(self.result)

		html = Template(context).render(
								result=self.result,
								device_count=len(self.devices),
								casecount=self.result['casecount'],
								totalcount=self.result['totalcount'],
								success=len(self.result['success']),
								failed=len(self.result['failed']),
								static_forder=self.static_forder
								)
		if report_path and not os.path.exists(report_path):
			os.makedirs(report_path)

		report = os.path.join(report_path or self.logdir,'report.html')
		with open(report,'w',encoding='utf-8') as f:
			f.write(html)

		self.result['duration'] = round(time.time() - self.current_time,2)
		self.result['report'] = report

		pprint(self.result)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-c",help="usage: python androidRunner -c [casename]")
	parser.add_argument("-o",help="open report.html when test_job is done")
	parser.add_argument("-d",help="specify used devices")
	parser.add_argument("-report",help="specify report path")
	parser.add_argument("-app",help="specify used apk")
	args = parser.parse_args()
	try:
		test_devices = None
		if args.d:
			test_devices = eval(args.d)
		runner = AndroidRunner(args.c,test_devices,args.app)
		runner.runMultiTest()
		runner.generateReport(args.report)
	except Exception as e:
		print(e)
		sys.exit(-1)
	#如果指定了-o参数,则运行结束启用默认浏览器打开测试报告 python androidRunner.py -o type_anything_here
	if args.o:
		if platform.system() == 'Windows':
			os.system('start %s' %runner.result['report'])
		else:
			os.system('open %s' %runner.result['report'])