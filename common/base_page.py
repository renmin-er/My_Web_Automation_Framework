# common/base_page.py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step("打开URL: {url}")
    def open_url(self, url: str):
        self.driver.get(url)

    # 我们可以把 find_element 拆分的更细
    def wait_for_element_visible(self, locator: tuple, timeout: int = 10):
        """等待元素在页面上可见"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            # ... 截图和报错逻辑 ...
            raise

    def wait_for_element_clickable(self, locator: tuple, timeout: int = 10):
        """等待元素变为可点击状态"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            # ... 截图和报错逻辑 ...
            raise

    @allure.step("点击元素: {locator}")
    def click(self, locator: tuple):
        """点击元素 (优化版)"""
        # 点击前，先等待元素变为可点击
        element = self.wait_for_element_clickable(locator)
        element.click()

    @allure.step("在元素 {locator} 中输入文本: {text}")
    def send_keys(self, locator: tuple, text: str):
        """输入文本 (优化版)"""
        # 输入前，先等待元素可见
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_title(self) -> str:
        return self.driver.title