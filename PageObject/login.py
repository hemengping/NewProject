import yaml
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

from mima import key_click

class LoginObject:
    def __init__(self):
        self.steps = yaml.safe_load(open('F:/python/NewProject/data/login_1.yaml', 'r',encoding='UTF-8'))
        print(self.steps)

    def login(self,driver:WebDriver):
        for step in self.steps:
            element = None
            if isinstance(step,dict):
                if "id" in step.keys():
                    try:
                        element = driver.find_element_by_id(step["id"])
                    except NoSuchElementException:
                        pass
                elif "text" in step.keys():
                    try:
                        textValue = step["text"]
                        element = driver.find_element_by_android_uiautomator(
                            f'new UiSelector().text("{textValue}")'
                        )
                    except NoSuchElementException:
                        pass

                elif "key" in step.keys():
                    key_click(driver,"aaaa1111")
                else:
                    print(step.keys())
                #元素交互
                if element is None:
                    pass
                elif "input" in step.keys():
                    element.send_keys(step["input"])
                elif "key" in step.keys():
                    pass
                else:
                    element.click()

if __name__ == "__main__":
    LoginObject().login()
