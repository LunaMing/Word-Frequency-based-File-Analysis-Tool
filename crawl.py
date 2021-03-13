from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys

# 打开浏览器 Chrome
browser = webdriver.Chrome()
# 准备网址
url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'

# 访问网址
browser.get(url)

# 获取元素
element_list = browser.find_elements_by_class_name('node-title')

# 计数
count = 0
# 拿到标题文字
for element in element_list:
    count += 1
    title = element.text
    print(str(count) + " : " + title)

    # 点击此元素
    # 使用ctrl+click
    # 跳转为后台新页面
    ActionChains(browser) \
        .key_down(Keys.CONTROL) \
        .click(element) \
        .key_up(Keys.CONTROL) \
        .perform()

# 退出整个浏览器
browser.quit()
