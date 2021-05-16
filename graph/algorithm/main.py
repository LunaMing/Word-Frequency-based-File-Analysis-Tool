import pdftotext

from algorithm import picture, word
from algorithm.word import preprocessing_str


def word_freq():
    total_str = ""
    total_str_list = []

    pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub"]
    for pdf_name in pdf_name_list:
        print("PDF: " + pdf_name)
        # 读取pdf文件
        pdf_path = "res/pdf/" + pdf_name + ".pdf"
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
        raw_str = ""
        for page in pdf:
            raw_str += str(page)
        # 预处理
        s = preprocessing_str(raw_str)
        # 计入总字符集
        total_str += s
        total_str_list.append(s)

    # 统计
    # word.count(total_str, "total.txt")
    word.total_count(total_str_list)
    # 可视化
    picture.cloud(total_str, "total.png")
