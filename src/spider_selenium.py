from selenium import webdriver


def crawl():
    browser = webdriver.Chrome()
    # 准备网址
    url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'

    # 访问网址
    browser.get(url)

    # 获取文章标题元素
    title_element_list = browser.find_elements_by_xpath('//*[@class="node-title"]/a')
    print("num of elements: " + str(len(title_element_list)))

    # 计数
    # 点击每个标题进行具体抓取
    for title_element in title_element_list:
        title = title_element.text
        print("title->" + title)
        paper_url = title_element.get_attribute('href')
        print(paper_url)

    # 退出整个浏览器
    browser.quit()


if __name__ == '__main__':
    crawl()
    exit()
