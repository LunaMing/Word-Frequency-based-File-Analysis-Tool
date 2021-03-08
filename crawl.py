from selenium import webdriver

# 打开一个浏览器
browser = webdriver.Chrome()
# 准备一个网址
url = 'https://dl.acm.org/doi/proceedings/10.1145/3387514'

# 访问网址
browser.get(url)
# 获取元素
element_list = browser.find_elements_by_class_name('issue-item__title')
# 拿到标题文字
for element in element_list:
    title = element.text
    print(title)

# 退出
browser.quit()
