import pdftotext
from nltk.corpus import stopwords


def word_deal(pdf_name: str):
    """ 文本处理对外接口

        包括pdf转txt、文本预处理。

        :param pdf_name: pdf文件名，不包含后缀。

    """
    txt_path = pdf2text(pdf_name)
    raw_str = open(txt_path, 'r', encoding='UTF-8').read()
    s = preprocessing(raw_str)
    return s


def pdf2text(pdf_name: str):
    """pdf转txt

       将pdf转为txt文件。其中格式原封不动按照pdf来做，换行或左右双排无法特殊识别。

       :param pdf_name: pdf文件名，不包含后缀
       :type pdf_name: str
       :returns: 生成的txt文件路径
       :rtype: str
       """

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

    print("PDF -> TXT : " + txt_path)
    return txt_path


def preprocessing(s: str):
    """预处理"""

    # 分词
    word_list = []
    words = s.split()
    for word in words:
        # 大于一个字母的单词才有意义
        if len(word) > 1:
            word_list.append(word)

    # 停用词表
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]

    # 组装结果
    res = ""
    for w in filtered_words:
        res = res + " " + w

    return res


def count(raw_txt: str):
    """统计文本频率"""
    print("-- COUNT --")

    # 拆分字符串
    word_list = []
    words = raw_txt.split()
    for word in words:
        word_list.append(word)

    # 统计
    counts = {}
    for word in word_list:
        counts[word] = counts.get(word, 0) + 1

    # 排序
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    # 打印结果 Top N
    N = 15
    for i in range(N):
        word, _count = items[i]
        print("{0:<10}{1:>5}".format(word, _count))

    # 输出结果到文件
    fo = open("../output/freq.txt", "w", encoding='UTF-8')
    for item in items:
        fo.write(str(item) + "\n")
    fo.close()
