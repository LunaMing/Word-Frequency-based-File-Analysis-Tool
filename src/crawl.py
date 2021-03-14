from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def crawl():
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
    # 第一个不是链接
    count = 1
    # 点击每个标题进行具体抓取
    while count < title_len:
        print("count: " + str(count))

        # 获取文章标题
        title_element = title_element_list[count]
        title = title_element.text
        print("title: " + title)

        while len(browser.window_handles) < 3:
            # 点击此元素
            # 使用ctrl+click
            # 跳转为后台新页面
            ActionChains(browser) \
                .key_down(Keys.CONTROL) \
                .click(title_element) \
                .key_up(Keys.CONTROL) \
                .perform()

        # 计算新页面的句柄数
        # 最后一个句柄就是新打开的页面
        index_new = len(browser.window_handles) - 1
        handle_new = browser.window_handles[index_new]
        # 窗口句柄切换到新页面
        browser.switch_to.window(handle_new)

        # 等待新页面加载完毕
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "file"))
            )

            file_text = element.text
            print(file_text)
        finally:
            browser.close()

        # 窗口句柄切换回到目录页面
        browser.switch_to.window(handle_old)

        # 计数+1
        count += 1

    # 退出整个浏览器
    browser.quit()
