import pdftotext
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


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

    # 去标点
    # 只保留“数量大于等于一个的字母或数字”
    # Create an instance of RegexpTokenizer for alphanumeric tokens
    tokeniser = RegexpTokenizer(r'\w+')
    # Tokenise
    tokens = tokeniser.tokenize(s)
    # print(tokens)

    # 词根化
    # Create an instance of WordNetLemmatizer
    lemmatiser = WordNetLemmatizer()
    # Lowercase and lemmatise tokens
    lemmas = [lemmatiser.lemmatize(token.lower(), pos='v') for token in tokens]
    # print(lemmas)

    # 停用词
    # Remove stopwords
    keywords = [lemma for lemma in lemmas if lemma not in stopwords.words('english')]
    # print(keywords)

    # 大于一个字母的单词才有意义
    word_list = [keyword for keyword in keywords if len(keyword) > 1]
    # print(word_list)

    # 组装结果
    res = ""
    for w in word_list:
        res = res + " " + w

    return res


def count(raw_txt: str, out_file: str):
    """统计文本频率"""
    print("-- COUNT --")

    # 拆分字符串
    word_list = raw_txt.split()

    # 统计
    counts = {word: word_list.count(word) for word in set(word_list)}

    # 排序
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    # 打印结果 Top N
    print(items)

    # 输出结果到文件
    fo = open("../output/" + out_file, "w", encoding='UTF-8')
    for item in items:
        fo.write(str(item) + "\n")
    fo.close()
