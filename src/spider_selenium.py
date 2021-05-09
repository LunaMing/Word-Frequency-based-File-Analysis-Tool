import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# 静默模式
options.add_argument('--headless')


def get_paper_urls(url):
    # 所有论文详情页面的url列表
    paper_urls = []

    # 启动浏览器
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    # 获取文章标题元素
    title_element_list = browser.find_elements_by_xpath('//*[@class="node-title"]/a')
    print("num of elements: " + str(len(title_element_list)))

    # 保存到总的url列表
    for title_element in title_element_list:
        paper_url = title_element.get_attribute('href')
        paper_urls.append(paper_url)

    # 退出整个浏览器
    browser.quit()

    return paper_urls


def paper_spider(paper_urls, debug=False):
    # 所有论文列表
    paper_list = []
    # 启动浏览器
    browser = webdriver.Chrome(options=options)

    i = 0
    for paper_url in paper_urls:
        if debug and i > 3:
            break
        print("-- start get paper " + str(i) + " ...")
        paper = get_paper_info(browser, paper_url)
        paper_list.append(paper)
        i += 1

    # 退出整个浏览器
    browser.quit()

    return paper_list


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

    # 合成论文对象
    paper = {
        "Title": title,
        "Author": author_school,
    }
    return paper


def output_csv(dict_data):
    csv_file_path = "../output/paper_info.csv"
    csv_columns = ['Title', 'Author']
    with open(csv_file_path, 'w', encoding='UTF-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)


if __name__ == '__main__':
    start_url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'

    # 从总会议网址出发，获取论文的所有url
    paper_url_list = get_paper_urls(start_url)

    # 每篇论文爬取具体信息
    # debug的时候只爬前几个论文
    paper_list = paper_spider(paper_url_list, debug=True)

    # 输出结果到文件
    output_csv(paper_list)

    exit()
