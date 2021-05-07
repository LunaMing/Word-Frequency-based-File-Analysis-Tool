from src import picture, word, myneo4j


# 爬虫
# crawl()

def word_freq():
    total_str = ""
    total_str_list = []

    pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub", "nsdi20spring_burnett_prepub"]
    for index in range(len(pdf_name_list)):
        pdf_name = pdf_name_list[index]
        # 文本处理
        s = word.word_deal(pdf_name)
        total_str += s
        total_str_list.append(s)
        # 统计
        word.count(total_str, pdf_name + ".txt")
        # 可视化
        picture.cloud(s, pdf_name + ".png")

    # 统计
    word.count(total_str, "total.txt")
    data = word.total_count(total_str_list)
    # 可视化
    picture.cloud(total_str, "total.png")
    picture.plotdata(data)


# 词频统计
word_freq()

# 可视化 neo4j
myneo4j.neo4j_driver()
