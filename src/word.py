import re

import pdftotext


def word_deal(pdf: str):
    txt_path = pdf2text(pdf)
    raw_str = open(txt_path, 'r', encoding='UTF-8').read()
    s = preprocessing(raw_str)
    count(s)
    return s


def pdf2text(pdf_name: str):
    # 读取pdf文件
    pdf_path = "../res/pdf/" + pdf_name + ".pdf"
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # 写入txt文件
    txt_path = "../res/txt/" + pdf_name + ".txt"
    fo = open(txt_path, "w", encoding='UTF-8')
    for page in pdf:
        fo.write(str(page) + "\n")
    fo.close()

    return txt_path


def preprocessing(s: str):
    # 特殊符号替换
    # 将文本中特殊字符替换为空格
    for ch in '!"#$%&()*+,-–−./:;<=>?@[\\]^_‘{|}~∼→•≤∗´”“\n':
        s = s.replace(ch, " ")
    # 将文本中数字替换为空格
    for ch in '0123456789':
        s = s.replace(ch, " ")

    # 只保留字母
    s = re.sub(r'[^A-Za-z ]+', '', s)

    # 改为全小写
    s = s.lower()
    return s


def count(raw_txt: str):
    print("-- COUNT --")

    words = raw_txt.split()

    # 停用词表
    word_list = []
    for word in words:
        word_list.append(word)

    # filtered_words = [word for word in word_list if word not in stopwords.words('english')]

    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(10):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word, count))

    # 打开一个文件
    fo = open("../output/freq.txt", "w", encoding='UTF-8')

    for item in items:
        fo.write(str(item) + "\n")

    # 关闭打开的文件
    fo.close()
