from selenium import webdriver

# 所有论文详情页面的url列表
paper_url_list = []


def crawl():
    browser = webdriver.Chrome()
    # 准备网址
    url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'
    # 访问网址
    browser.get(url)

    # 获取文章标题元素
    title_element_list = browser.find_elements_by_xpath('//*[@class="node-title"]/a')
    print("num of elements: " + str(len(title_element_list)))

    # 保存到总的url列表
    for title_element in title_element_list:
        paper_url = title_element.get_attribute('href')
        paper_url_list.append(paper_url)

    # 退出整个浏览器
    browser.quit()


def paper_spider():
    print("-- paper spider --")
    for paper_url in paper_url_list:
        print(paper_url)


if __name__ == '__main__':
    crawl()
    paper_spider()
    exit()
