from src.picture import cloud
from src.word import word_deal

# 爬虫
# crawl()

pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub", "nsdi20spring_burnett_prepub"]
for index in range(len(pdf_name_list)):
    pdf_name = pdf_name_list[index]
    # 文本处理
    s = word_deal(pdf_name)
    # 可视化
    cloud(s, pdf_name + ".png")
