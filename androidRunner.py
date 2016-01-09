#coding:utf-8
import sys,os,time,requests,platform
from configs.androidConfig import casepath,\
									casedatapath,\
									logpath,\
									snapshotpath,\
									case_logmode,\
									appium_log_level,\
									devices,\
									shared_capabilities,\
									case_elements,\
									test_datas,\
									conflict_datas
sys.path.append(casepath)
from main import Logger,TestData,CaseElements
from threading import Thread
from datetime import datetime
from pprint import pprint

class AndroidRunner(object):
	def __init__(self,singlecase=None):
		self.singlecase = singlecase
		self.current_system = platform.system()
		self.case_elements = CaseElements(case_elements)
		self.test_datas = TestData(test_datas)
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
				"totalcount":0,
				"casecount":0,
				"duration":0,
				"report":None
		}
		self._initcase(singlecase)
		self._initdirs()

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
			self.devices[index] = device
			port = str(13230 + index)
			bootstrap_port = str(14230 + index)
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
		appium_thread_list = []
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
			t = Thread(target=os.system,args=(cmd,))
			t.daemon = True
			appium_thread_list.append(t)
			if self.is_Appium_Alive(case.appium_port):
				self.stopAppium()

		for t in appium_thread_list:
			t.start()

		for case in cases:
			starts = time.time()
			while time.time() - starts < timeout:
				if self.is_Appium_Alive(case.appium_port):
					print("[success]Appium started on port : %s bootstrap_port: %s for device %s" %(case.appium_port,case.bootstrap_port,case.device_name))
					break
				else:
					time.sleep(0.5)
			else:
				print("[failure]Start Appium failed on port: %s bootstrap_port: %s !" %(case.appium_port,case.bootstrap_port))
				self.stopAppium()
				sys.exit(-1)

	def stopAppium(self):
		'''
			关闭所有appium服务
		'''
		if self.current_system == 'Windows':
			os.system("taskkill /F /IM node.exe")
		else:
			os.system("pkill -f appium")

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
		start = time.time()
		caselog = os.path.join(self.logdir,case.casename+"_case")
		logger = Logger(caselog,case_logmode)
		setattr(case,'logger',logger)
		setattr(case, 'result', {"errorMsg":None})
		setattr(case, 'appiumlogfile', os.path.join(self.logdir,case.device_name+"_"+case.appium_port+case.filename+"_appium.log"))
		setattr(case,'caselogfile',caselog+"_info.log")
		setattr(case,'case_elements',self.case_elements)
		setattr(case,'test_datas',self.test_datas)
		case = case(datas)
		try:
			print("running test:%s %s" %(case.casename,case.desc))
			case.run()
		except Exception as e:
			errorMsg = str(e)
			case.logger.log("[ERROR]%s" %errorMsg)
			case.save_screen("error")
			case.result['result'] = False
			case.result['errorMsg'] = errorMsg
			self.result['failed'].append(case)
		finally:
			end = time.time()
			case.result['runtime'] = round(end-start,2)
			print("end test:",case.casename)
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

	def generateReport(self):
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
		report = os.path.join(self.logdir,'report.html')
		with open(report,'w',encoding='utf-8') as f:
			f.write(html)

		self.result['duration'] = round(time.time() - self.current_time,2)
		self.result['report'] = report

		pprint(self.result)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-c",help="usage: python androidRunner -case [casename]")
	parser.add_argument("-o",help="auto open report.html when test_job is done")
	args = parser.parse_args()

	runner = AndroidRunner(args.c)
	runner.runMultiTest()
	runner.generateReport()
	#如果命令行参数大于1个,用默认浏览器打开测试报告 python androidRunner.py type_anything_here
	if args.o:
		os.system('start %s' %runner.result['report'])