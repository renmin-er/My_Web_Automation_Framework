import pytest
from selenium import webdriver
from pages.search_page import SearchPage
import allure
import time
import os


# test_cases/test_01_search.py

# ... (imports) ...

# test_cases/test_01_search.py

@pytest.fixture(scope="class")
def class_fixture():  # 或者你的 fixture 名字
    """
    工业级健壮版的 Fixture
    """
    print("\n--- [Fixture Setup] Starting setup... ---")
    driver = None  # 先初始化为 None

    try:
        # --- 1. 启动浏览器，这是最可能出错的地方 ---
        print("--- [Fixture Setup] Initializing Chrome WebDriver... ---")
        options = webdriver.ChromeOptions()
        # 忽略证书错误，这在CI环境中很重要
        options.add_argument('--ignore-certificate-errors')

        if os.getenv('IS_JENKINS') == 'true':
            print("--- [Fixture Setup] Jenkins environment detected. Applying headless options... ---")
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')

        driver = webdriver.Chrome(options=options)
        print("--- [Fixture Setup] WebDriver initialized successfully. ---")

        driver.maximize_window()

        # --- 2. 准备页面对象 ---
        search_page = SearchPage(driver)

        # --- 3. 打开初始页面并验证 ---
        print(f"--- [Fixture Setup] Opening URL: https://www.baidu.com ---")
        driver.get("https://www.baidu.com")
        assert "百度" in driver.title, f"FATAL: Failed to open Baidu. Current title: '{driver.title}'"
        print(f"--- [Fixture Setup] Page opened successfully. Title: {driver.title} ---")

        # --- 4. 将准备好的资源传递出去 ---
        yield (driver, search_page)

    except Exception as e:
        # 如果 try 块中任何一步出错（特别是 webdriver.Chrome()），就在这里捕获
        print(f"\n!!!!!! FATAL ERROR in Fixture Setup !!!!!!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        # 抛出 pytest.fail，这将立即终止测试会话，并将构建标记为失败
        pytest.fail("Fixture setup failed, see console output for details.", pytrace=False)

    finally:
        # --- 5. 无论成功与否，都尝试清理资源 ---
        print("\n--- [Fixture Teardown] Starting teardown... ---")
        if driver:
            time.sleep(2)
            driver.quit()
            print("--- [Fixture Teardown] WebDriver quit successfully. ---")
        else:
            print("--- [Fixture Teardown] No driver instance to quit. ---")

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