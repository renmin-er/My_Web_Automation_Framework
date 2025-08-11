import pytest
import os
if __name__ == '_main_':
    pytest.main([
        '-sv',
        './test_cases',
        '--alluredir=./reports/allure-results',  # 指定Allure原始数据目录
        '--clean-alluredir'  # 每次运行前清空该目录
    ])
