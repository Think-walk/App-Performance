#!/usr/bin/python3
#coding:utf-8
import os
import sys
import time
import datetime
import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

packageA = "com.test.voice.chat"
os.system("appium -a 127.0.0.1 -p 4723  --log xxx.log --local-timezone &")
class OperationA(unittest.TestCase):
    @classmethod
    def setUp(self):
        desired_caps = {}
        #desired_caps['unicodeKeyboard'] = True # 设置输入编码默认格式 这个一般在输入中文字符的时候会用到
        #desired_caps['resetKeyboard'] = True
        desired_caps['noReset'] = 'True'    #防止退出driver时应用被重置
        desired_caps['platformName'] = 'Android' #设置平台
        desired_caps['platformVersion'] = '7.1.1' #系统版本
        desired_caps['deviceName'] = 'ZY322RKSQN' #设备id
        desired_caps['autoLaunch'] = 'True' #是否自动启动
        #desired_caps['app'] = PATH('Test.apk' ) #安装包路径，放在该py文件的目录下
        desired_caps['appPackage'] = 'com.test.voice.chat' #包名
        desired_caps['appActivity'] = 'com.test.voice.chat.main.SplashActivity' #启动的activity

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit() #case执行完退出

    def test_A_dpApp(self): #需要执行的case
        self.driver.implicitly_wait(10) # 操作：在10秒内当找到下一步的元素信息就立刻执行下一步，不会等待10秒执行设置一次所有方法都生效
#        el = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/btnPhoneLogin']") #通过xpath找到定位
#        el.click() #点击定位元素
#        self.driver.implicitly_wait(10)
#        el1 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/country_code']")
#        el1.click()
#        self.driver.implicitly_wait(10)
#        el2 = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'China')]")
#        el2.click()
#        self.driver.implicitly_wait(10)
#        self.driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.test.voice.chat:id/phone_number_edit']").send_keys("18825871965")
#        self.driver.implicitly_wait(10)
#        el3 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/btnLogin']")
#        el3.click()
#        self.driver.implicitly_wait(10)
#        for i in range(1,7):
#            self.driver.find_element_by_xpath("//android.widget.EditText[contains(@index,'"+str(i)+"')]").send_keys(""+str(i)+"")
#        self.driver.implicitly_wait(2)
        try:
            el4 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivClose']")
            if is_element_exist(el4) == True:
                el4.click()
        except Exception as e:
            print(e,"未发现活动弹窗！")
        self.driver.implicitly_wait(2)
        try:
            el5 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/icGiftCancel']")
            if is_element_exist(el5) == True:
                el5.click()
        except Exception as e:
            print(e,"未发现签到弹窗！")
        time.sleep(10)  #第一个tab静止10秒等待页面数据加载完毕
        #self.driver.tap([(107,457)],500) #点击第一个麦位
        #ActionChains(self.driver).move_by_offset(107,457).click().perform()
#        self.driver.implicitly_wait(2)
#        try:
#            el8 = self.driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']")
#            if is_element_exist(el8) == True:
#                el8.click()
#        except Exception as e:
#            print(e,"未发现mic授权弹窗！")
#        self.driver.implicitly_wait(2)
#        try:
#            el9 = self.driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']")
#            if is_element_exist(el9) == True:
#                el9.click()
#        except Exception as e:
#            print(e,"未发现存储授权弹窗！")
#        self.driver.keyevent(4)  #系统返回键
#        self.driver.tap([(541,659)],500) #点击最小化房间
        el6 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/tvMatch']")
        el6.click()
        time.sleep(10)  #第二个tab静止10秒等待页面数据加载完毕
#        el7 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/tvMoment']")
#        el7.click()
#        time.sleep(10)  #第三个tab静止10秒等待页面数据加载完毕
        el8 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivMessage']")
        el8.click()
        time.sleep(10)  #第四个tab静止10秒等待页面数据加载完毕
        el9 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/button3']")
        el9.click()
        time.sleep(10)  #第五个tab静止10秒等待页面数据加载完毕
        el10 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/tvMain']")
        el10.click()
        el11 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivEnter']")
        el11.click()
        #self.driver.swipe(433, 900, 433, 600, 500)  #向上滑动页面
#        el12 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivGift']")
#        el12.click()
#        el13 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivAllArr']")
#        el13.click()
#        el14 = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@index,'1')]")
#        el14.click()
#        el15 = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'DOve')]")
#        el15.click()
#        el16 = self.driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.test.voice.chat:id/ivCountArr']")
#        el16.click()
#        el17 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/tvSend']")
#        el17.click()
#        time.sleep(3)
#        el18 = self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/tvNum']")
#        for i in range(0,24):
#            el18.click()
#            i = i+1
        time.sleep(30)
    #判断元素是否存在
    def is_element_exist(self,element,timeout=5):
        count = 0
        while count < timeout:
            souce = self.driver.page_source
            print(source)
            if element in souce:
                return  True
            else:
                count += 1
                time.sleep(1)
                return False
#    def CheckLogOut(self):
#        while True:
#            wait = WebDriverWait(self.driver, 1200, 1).until(lambda x:x.find_element_by_xpath("//android.widget.FrameLayout[@resource-id='com.test.voice.chat:id/dialog_boby']"))    # 调用driver, 1200秒内 ，每1秒寻找一次
#            if wait:
#                self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.test.voice.chat:id/dialog_nagative']").click()
#                print("发现退出弹框并关闭弹框!")
#                #time.sleep(5)

def runA():
    os.system("appium -a 127.0.0.1 -p 4723  --log xxx.log --local-timezone &")
    time.sleep(5)
    suite = unittest.TestLoader().loadTestsFromTestCase(OperationA)
    unittest.TextTestRunner(verbosity=2).run(suite) #执行所有case集
    print('结束子线程A！')
    sys.exit(2)
    
if __name__ == "__main__":
    runA()
