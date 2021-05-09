from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# 静默模式
options.add_argument('--headless')

# 所有论文详情页面的url列表
paper_url_list = []
# 所有论文列表
paper_list = []


def get_paper_urls(url):
    # 启动浏览器
    browser = webdriver.Chrome(options=options)
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
    # 启动浏览器
    browser = webdriver.Chrome(options=options)

    i = 0
    for paper_url in paper_url_list:
        print("-- start get paper " + str(i) + " ...")
        get_paper_info(browser, paper_url)
        i += 1

    # 退出整个浏览器
    browser.quit()


def get_paper_info(browser, paper_url):
    print(paper_url)
    browser.get(paper_url)

    # 获取论文标题
    title_element = browser.find_element_by_xpath('//*[@id="page-title"]')
    title = title_element.text

    # 获取论文作者
    author_element_list = browser.find_elements_by_xpath(
        '//*[@class="field field-name-field-paper-people-text field-type-text-long field-label-above"]/div')
    author_school = author_element_list[1]

    # 合成论文对象，放入总列表
    paper = {
        "title": title,
        "author": author_school,
    }
    paper_list.append(paper)


if __name__ == '__main__':
    start_url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'
    get_paper_urls(start_url)
    paper_spider()

    # 输出结果到文件
    fo = open("../output/paper_info.csv", "w", encoding='UTF-8')

    for p in paper_list:
        # json_data = json.dumps(p)
        # fo.write(json_data)
        fo.write("title: " + p["title"] + "\n")

    fo.close()

    exit()
