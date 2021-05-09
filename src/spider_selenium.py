from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# 静默模式
options.add_argument('--headless')

# 所有论文详情页面的url列表
paper_url_list = []
# 所有论文列表
paper_list = []


class Paper:
    title = ""
    abstract = ""
    author = ""


def get_paper_urls(url):
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
    for paper_url in paper_url_list:
        print(paper_url)
        p = Paper()
        p.title = get_paper_title(paper_url)
        paper_list.append(p)


def get_paper_title(paper_url):
    browser = webdriver.Chrome(options=options)
    browser.get(paper_url)

    # 获取论文标题
    title_element = browser.find_element_by_xpath('//*[@id="page-title"]')
    title = title_element.text

    # 获取论文作者
    author_element_list = browser.find_elements_by_xpath(
        '//*[@class="field field-name-field-paper-people-text field-type-text-long field-label-above"]/div')
    author_school = author_element_list[1]
    print(author_school.text)

    # 退出整个浏览器
    browser.quit()
    return title


if __name__ == '__main__':
    start_url = 'https://www.usenix.org/conference/nsdi20/accepted-papers'
    get_paper_urls(start_url)
    paper_spider()
    for paper in paper_list:
        print(paper.title)
    exit()
