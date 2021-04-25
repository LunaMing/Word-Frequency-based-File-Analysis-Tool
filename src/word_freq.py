import re

import wordcloud


def get_text():
    txt = open('../res/raw.txt', 'r', encoding='UTF-8').read()

    # 特殊符号替换
    # 将文本中特殊字符替换为空格
    for ch in '!"#$%&()*+,-–−./:;<=>?@[\\]^_‘{|}~∼→•≤∗´”“\n':
        txt = txt.replace(ch, " ")
    # 将文本中数字替换为空格
    for ch in '0123456789':
        txt = txt.replace(ch, " ")

    # 只保留字母
    txt = re.sub(r'[^A-Za-z ]+', '', txt)

    # 改为全小写
    txt = txt.lower()

    return txt


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
    fo = open("../res/word_result.txt", "w", encoding='UTF-8')

    for item in items:
        fo.write(str(item) + "\n")

    # 关闭打开的文件
    fo.close()


def get_cloud(s):
    w = wordcloud.WordCloud(background_color='white')
    w.generate(s)
    w.to_file('../res/output.png')
