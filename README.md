# defender

简单讲一下用法吧：

一：环境准备：

    1、搭建appium的环境，确保appium在dos下可以通过命令启动：appium -a localhost -p 14230

    2、搭建python3.x 环境，对，就是python2.x不支持！ 建议使用python3.3.5，安装pip

    3、进入defender根目录，安装defender的python模块： pip install -r requirements.txt


二：配置defender

    找到配置文件defender/configs/androidConfig.py  按需配置

三：写case

    参考 defender/testcases/下的测试用例，可以直接拷贝后只需修改用例内 desc和run()方法内的执行步骤

四：运行测试

    在defender目录dos下运行：

        python androidRunner.py   运行结束后dos窗口最后会输出测试结果（包含测试报告的路径，打开后可以查看详细结果）

        python androidRunner.py -c casename  执行运行某一条case使用带参数的方式运行的话，在测试结束后会自动启动默认浏览器打开测试报告（建议体验下）

		python androidRunner.py -o [任意字符] -o后接任意参数:在测试结束后会自动启动默认浏览器打开测试报告（建议体验下,-c -o 可同时使用）

		
五：用例写法

	defender/testcases目录下有示例脚本，可参考着写
	
	case内写 点击app上id/class_name/...是'click_me'元素的不同写法

		1、self.find_element_by_id('click_me').click()	|	self.find_element_by_class_name('click_me').click()  | ....   同webdriver的方法，需要敲比较多键盘 = =。
		
		2、self.find('id',id).click()	或者  self.click('id','click_me')   |	self.find('class_name','click_me').click()	或者	self.click('class_name','click_me')
		
		3、self.super_click('点我')  <---  这种方式需要先将元素信息在androidConfig.py的case_elements配置项内配好，该方式实现了app元素和case的分离，推荐使用！

六：测试报告（report.html 静态页面）

	1、case总数，case运行时间以及哪个case在哪台设备上运行失败(成功) 信息一目了然

	2、每个case测试过程中与不同设备产生的appium日志 一键查看
	
	3、测试中case本身执行产生的日志(记录case操作手机时执行的动作日志)
	
	4、测试中每个case产生的截图 一键查看
		
六：其他：

    目前支持多case、多设备
	
	适用场景：

		1、单个手机跑多个功能测试case，并生成测试报告

		2、同一个功能测试case同时在多个手机上跑，并生成测试报告

		3、多个功能测试的case同时在多个手机上顺序执行，并生成测试报告

			说明：电脑连接了两个手机，在androiConfig.py中的devices配置上两个手机的参数，如果testcases目录下有3个针对不同功能的脚本test01.py test02.py test03.py

			运行python androidRunner.py后，将会同时在两个手机上先运行test01.py进行测试，接着运行test02.py，最后运行test03.py，最后输出整体测试报告





