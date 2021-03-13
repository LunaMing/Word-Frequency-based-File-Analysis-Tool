from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys

# 打开浏览器 Chrome
browser = webdriver.Chrome()
# 准备网址
url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'

# 访问网址
browser.get(url)

# 记录目录页handle
handle_old = browser.window_handles[0]

# 获取文章标题元素
title_element_list = browser.find_elements_by_class_name("node-title")
# 文章标题元素数量
title_len = len(title_element_list)
print("num of articles: " + str(title_len))

# 计数
count = 0
# 点击每个标题进行具体抓取
for count in range(title_len):
    print("count: " + str(count))

    # 获取文章标题
    title_element = title_element_list[count]
    title = title_element.text
    print("title: " + title)

    # 点击此元素
    # 使用ctrl+click
    # 跳转为后台新页面
    ActionChains(browser) \
        .key_down(Keys.CONTROL) \
        .click(title_element) \
        .key_up(Keys.CONTROL) \
        .perform()

    # 等待新页面加载完毕
    # 显示等待10秒
    browser.implicitly_wait(10)

    # todo 有几个新页面没有打开？
    # 计算新页面的句柄数
    # 最后一个句柄就是新打开的页面
    index_new = len(browser.window_handles) - 1
    handle_new = browser.window_handles[index_new]
    # 窗口句柄切换到新页面
    browser.switch_to.window(handle_new)

    # 获取摘要元素
    abstract_elem = browser.find_element_by_xpath(
        "/html/body/div[1]/div/main/div[2]/article/div[2]/div[2]/div[2]/div[1]/div/div[2]/p")
    abstract = abstract_elem.text
    # 打印摘要文本
    print("abstract: " + abstract)

    # 退出这个页面
    # browser.close()

    # 窗口句柄切换回到目录页面
    browser.switch_to.window(handle_old)

    # 计数+1
    count += 1

# 退出整个浏览器
browser.quit()
