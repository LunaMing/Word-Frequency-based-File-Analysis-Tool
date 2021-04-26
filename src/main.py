from src.picture import cloud
from src.word import word_deal, count

# 爬虫
# crawl()

total_str = ""
pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub", "nsdi20spring_burnett_prepub"]
for index in range(len(pdf_name_list)):
    pdf_name = pdf_name_list[index]
    # 文本处理
    s = word_deal(pdf_name)
    total_str += s
    # 可视化
    count(total_str, pdf_name + ".txt")
    cloud(s, pdf_name + ".png")
count(total_str, "total.txt")
cloud(total_str, "total.png")
