from selenium.webdriver.common.by import By
from common.base_page import BasePage

"""
   只定义元素和操作，没有任何测试逻辑 
"""
class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, 'chat-textarea')
    SEARCH_BUTTON = (By.ID, 'chat-submit-button')
    def search(self,keyword:str):
        self.send_keys(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)