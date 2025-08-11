import pytest
from selenium import webdriver
from pages.search_page import SearchPage
import allure
import time
import os


# test_cases/test_01_search.py

# ... (imports) ...

@pytest.fixture(scope="class")
def class_fixture():  # 或者你的 fixture 名字，比如 search_page_fixture
    """
    这个 Fixture 负责创建和销毁浏览器实例和页面对象。
    """
    print("\n--- [Fixture Setup] Creating browser and Page Object ---")
    options = webdriver.ChromeOptions()

    # ================= 关键的修复在这里！ =================
    # 添加一个参数，忽略证书相关的错误
    options.add_argument('--ignore-certificate-errors')
    # 有时也需要下面这个参数
    options.add_argument('--allow-insecure-localhost')
    # =======================================================

    if os.getenv('IS_JENKINS') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # -----------------------------------------------------------
    # 为了调试，我们可以在这里加一个断言，确保页面真的打开了
    driver.get("https://www.baidu.com")
    assert "百度" in driver.title, f"页面打开失败，当前标题是: {driver.title}"
    print(f"成功打开页面，标题是: {driver.title}")
    # -----------------------------------------------------------

    search_page = SearchPage(driver)

    # 不同的 fixture 写法，返回不同的资源
    # 如果你的测试用例是 def test_... (self, class_fixture):
    yield (driver, search_page)
    # 如果你的测试用例是 def test_... (self, search_page_fixture):
    # yield search_page

    # --- Teardown ---
    print("\n--- [Fixture Teardown] Closing browser ---")
    time.sleep(2)
    driver.quit()


# ... 你的测试类和测试方法 ...
# 确保你的测试用例中不再调用 open_url，因为我们已经在 fixture 中打开了
# def test_search_selenium(self, class_fixture):
#     driver, search_page = class_fixture
#     # with allure.step("第一步，打开百度首页"):
#     #     search_page.open_url("https://www.baidu.com") # <--- 注释掉或删掉这行


@allure.feature("百度搜索功能")
class TestBaiduSearch:

    # ------------------- 第二步：改造测试方法 -------------------
    @allure.story("基础搜索场景")
    @allure.title("测试搜索'Selenium'关键字")
    def test_search_selenium(self, class_fixture):  # <--- 将 Fixture 作为参数传入
        """
        1.打开百度首页
        2.搜索关键字”selenium“
        """
        # 从传入的 fixture 参数中解包出我们需要的资源
        driver, search_page = class_fixture

        with allure.step("第一步，打开百度首页"):
            search_page.open_url("https://www.baidu.com")

        with allure.step("第二步，输入’selenium‘并点击搜索"):
            search_page.search("Selenium")

        with allure.step("第三步：断言结果"):
            time.sleep(2)
            page_title = search_page.get_title()
            allure.attach(page_title, name="搜索结果页面标题")
            assert "Selenium" in page_title, f"页面标题 '{page_title}' 不包含 'Selenium'"