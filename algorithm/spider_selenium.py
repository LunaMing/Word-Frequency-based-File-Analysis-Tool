import csv
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_paper_urls(browser, url):
    # 打开网页
    browser.get(url)

    # 获取文章标题元素
    title_element_list = browser.find_elements_by_xpath('//*[@class="node-title"]/a')
    print("num of elements: " + str(len(title_element_list)))

    # 所有论文详情页面的url列表
    paper_urls = []
    # 保存
    for title_element in title_element_list:
        paper_url = title_element.get_attribute('href')
        paper_urls.append(paper_url)

    return paper_urls


def paper_spider(browser, paper_urls, debug=False):
    # 所有论文列表
    papers = []

    for i in range(len(paper_urls)):
        if debug and i < 61:
            continue
        print("-- start get paper " + str(i) + " ...")
        paper = get_paper_info(browser, paper_urls[i])
        papers.append(paper)

    return papers


def text_remove_useless(text):
    # 分割逗号和分号
    authors = re.split('[,;]', text)

    # 去掉“and ”分割
    for i in range(len(authors)):
        old_a = authors[i]
        new_a_list = old_a.split("and ")
        if len(new_a_list) == 2:
            authors.remove(old_a)
            for new_a in new_a_list:
                if len(new_a) > 1:
                    authors.insert(i, new_a)

    # 去掉两边的空格
    for i in range(len(authors)):
        authors[i] = authors[i].strip()

    # 去除只有空字符的
    authors = [author for author in authors if len(author) > 0]

    return authors


def get_paper_info(browser, paper_url):
    print(paper_url)
    # 打开网页
    browser.get(paper_url)

    # 获取论文标题
    title_element = browser.find_element_by_xpath('//*[@id="page-title"]')
    title = title_element.text

    # 获取论文作者
    author_element_list = browser.find_elements_by_xpath(
        '//*[@class="field field-name-field-paper-people-text field-type-text-long field-label-above"]/div')
    author_school = author_element_list[1]

    # 获取斜体字的学校名称
    ems = author_school.find_elements_by_xpath(
        '/html/body/div[2]/main/section/div[3]/article/div/div[1]/div[2]/div/p/em')
    school_text = ""
    for em in ems:
        school_text += em.text
        school_text += " , "
    schools = text_remove_useless(school_text)

    # 获取作者和学校混杂
    author_text = author_school.text
    authors = text_remove_useless(author_text)
    # todo 建立学校和作者之间的关系：学校前面【到另一个学校名之间】的作者就属于后一个学校
    # 去除学校只保留作者名
    authors = [author for author in authors if author not in schools]

    # 获取论文摘要
    element_list = browser.find_elements_by_xpath(
        '//*[@class="field field-name-field-paper-description field-type-text-long field-label-above"]/div')
    abstract = element_list[1].text

    # 合成论文对象
    paper = {
        "Title": title,
        "Author": authors,
        "School": schools,
        "Abstract": abstract
    }
    return paper


def output_csv(dict_data):
    csv_file_path = "../output/paper_info.csv"
    csv_columns = ['Title', 'Author', 'School', 'Abstract']
    with open(csv_file_path, 'w', encoding='UTF-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)


if __name__ == '__main__':
    # 准备浏览器设置
    options = Options()
    # 静默模式
    options.add_argument('--headless')
    # 启动浏览器
    chrome = webdriver.Chrome(options=options)

    # 从总会议网址出发，获取论文的所有url
    start_url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'
    paper_url_list = get_paper_urls(chrome, start_url)

    # 每篇论文爬取具体信息
    # debug的时候只爬前几个论文
    paper_list = paper_spider(chrome, paper_url_list, debug=False)

    # 输出结果到文件
    output_csv(paper_list)

    # 退出整个浏览器
    chrome.quit()

    exit()
