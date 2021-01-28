import yaml as yaml
from appium import webdriver
import pytest
import yaml
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

from mima import get_number_keyboard_location,key_click
class TestYsApp:
    data = yaml.safe_load(open('data.yaml','r'))
    print(data)

    @classmethod
    def setup_class(cls):
        cls.capabilities={
            "platformName": "Android",
            "deviceName": "83f9f7d3",
            "appPackage": " com.ysepay.mobileportal.activity",
            "appActivity": ".IndexActivity",
            "noReset": "true"
        }
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub',cls.capabilities)
        cls.driver.implicitly_wait(20)

    @pytest.mark.parametrize("username,password",data)
    def test_login(self,username,password):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("我的")'
        ).click()

    #登录页有账户的页面
    def test_login_havaCount(self):
        self.driver.implicitly_wait(20)

        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("请输入登录密码")'
        ).click()
        self.driver.implicitly_wait(20)
        key_click(self.driver, 'aaaa1111')
        self.driver.find_element_by_id('com.ysepay.mobileportal.activity:id/prot_agreement').click()

        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("安全登录")'
        ).click()

    @pytest.mark.parametrize("username,password", data)
    def test_login_nothaveCount(self,username,password):
        try:
            self.driver.find_element_by_android_uiautomator(
                'new UiSelector().text("切换账号")'
            ).click()
        except NoSuchElementException:
            pass
        self.driver.find_element_by_id('com.ysepay.mobileportal.activity:id/loginUserNameEdit').send_keys(username)
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("请输入密码/验证码")'
        ).click()
        key_click(self.driver, 'aaaa1111')

        self.driver.find_element_by_id('com.ysepay.mobileportal.activity:id/prot_agreement').click()
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().text("安全登录")'
        ).click()

    @classmethod
    def teardown_class(cls):
        pass


