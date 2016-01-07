from android.basecase import AndroidDevice

class TestCase(AndroidDevice):
	# 需要修改  desc：描述这个测试脚本测试的内容
	desc = "答疑流程是否正常"

	def __init__(self,ce,dc):
		self.dc = dc
		self.appium_port = ce['port']
		self.device_name = dc['deviceName']
		self.appium_url = ce['url']
		self.casename = '%s_%s_%s' %(dc['deviceName'],ce['port'],str(self.__class__).split('.')[0].split('\'')[1])

	def __call__(self):
		super(TestCase,self).__init__(command_executor=self.appium_url,desired_capabilities=self.dc)
		return self

	# 需要修改
	def run(self):
		self.implicitly_wait(10)

		#允许使用摄像头
		self.click('id','android:id/button1',nocheck=True)
		#不注册点击登录
		self.click('id','com.wenba.bangbang:id/register_loginTv')
		#输入账号
		self.input('id','com.wenba.bangbang:id/login_username_et','11266661001')
		#输入密码
		self.input('id','com.wenba.bangbang:id/login_passwd_et','111111 ')
		#点击登录按钮
		self.click('id','com.wenba.bangbang:id/login_login_tv1')

		self.save_screen()

		#点击拍照搜题
		self.click('id','com.wenba.bangbang:id/skin_home_btn_camera')
		#允许调用摄像头
		self.click('id','android:id/button1',nocheck=True)
		#点击相册
		self.click('id','com.wenba.bangbang:id/campage_btn_pic')
		#找到相册内所有图片
		eles = self.finds('id','com.android.documentsui:id/icon_thumb')
		#选择第一张点击
		eles[1].click()
		#点击提交按钮
		self.click('id','com.wenba.bangbang:id/skin_edit_opt_submit')
		#点击老师答疑
		self.click('id','com.wenba.bangbang:id/skin_feed_search_buttom_live_layout')
		#同意调用录音
		self.click('id','android:id/button1',nocheck=True)
		#等直到出现取消发红包按钮
		btn = self.waitfor('id','com.wenba.bangbang:id/btn_cancel',timeout=120)
		btn.click()
		#评星级
		ele = self.finds('class_name','android.widget.ImageView')
		#五星
		ele[4].click()
		#点评内容
		self.input('id','com.wenba.bangbang:id/skin_edt_comment',"good good study day day up")
		#提交点评
		self.click('id','com.wenba.bangbang:id/skin_btn_rate_submit')
