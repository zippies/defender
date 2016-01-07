# defender

简单讲一下用法吧：
一：环境准备：
1、搭建appium的环境，确保appium在dos下可以通过命令启动：appium -a localhost -p 14230
2、搭建python3.x 环境，对，就是python2.x不支持！ 建议使用python3.3.5，安装pip
3、进入defender根目录，安装defender的python模块： pip install -r requirements.txt

二：配置defender
    找到配置文件defender/configs/androidConfig.py  按需配置
    
三：写case
    参考 defender/testcases/下的测试用例，可以直接拷贝后只需修改用例内的desc和run()方法内的执行步骤
  
四：运行测试
    在defender目录dos运行：
        python androidRunner.py   运行结束后dos窗口最后会输出测试结果（包含测试报告的路径，打开后可以查看详细结果）
        python androidRunner.py any_code   使用带参数的方式运行的话，在测试结束后会自动启动默认浏览器打开测试报告（建议体验下）
    
说明：
  目前支持多case、多设备
  实例场景：
      电脑连接了两个手机，在androiConfig.py中的devices配置上两个手机的参数，如果testcases目录下有3个针对不同功能的脚本01.py 02.py 03.py
      运行python androidRunner.py后，将会同时在两个手机上先运行01.py进行测试，接着运行02.py，最后运行03.py，最后输出报告
      
