import re

import pdftotext


def pdf2text(pdf_name, txt_name):
    pdf_path = "../res/pdf/" + pdf_name

    # Load your PDF
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # # If it's password-protected
    # with open("secure.pdf", "rb") as f:
    #     pdf = pdftotext.PDF(f, "secret")

    # How many pages?
    print(len(pdf))

    # Iterate over all the pages
    for page in pdf:
        print(page)

    # Read some individual pages
    print(pdf[0])
    print(pdf[1])

    # Read all the text into one string
    print("\n\n".join(pdf))

    # 打开一个文件
    txt_path = "../output/" + txt_name
    fo = open(txt_path, "w", encoding='UTF-8')

    for page in pdf:
        fo.write(str(page) + "\n")

    # 关闭打开的文件
    fo.close()


def get_text(txt_name):
    txt_path = '../output/' + txt_name
    txt_string = open(txt_path, 'r', encoding='UTF-8').read()
    preprocessing(txt_string)
    return txt_string


def preprocessing(s):
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


def word_deal(raw_txt):
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
    fo = open("../output/word_result.txt", "w", encoding='UTF-8')

    for item in items:
        fo.write(str(item) + "\n")

    # 关闭打开的文件
    fo.close()
