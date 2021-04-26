import pandas as pd
import pdftotext
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


def word_deal(pdf_name: str):
    """ 文本处理对外接口

        包括pdf转txt、文本预处理。

        :param pdf_name: pdf文件名，不包含后缀。

    """
    txt_path = pdf2text(pdf_name)
    raw_str = open(txt_path, 'r', encoding='UTF-8').read()
    s = preprocessing_str(raw_str)
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


def preprocessing_str(s: str):
    """预处理，包括组装字符串"""
    # 预处理
    word_list = preprocessing(s)
    # 组装结果
    res = ""
    for w in word_list:
        res = res + " " + w
    return res


def get_wordnet_pos(tag):
    """获取单词的词性"""
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def preprocessing(s: str):
    """预处理"""

    # 小写
    s = s.lower()

    # 去标点
    # 只保留“数量大于等于一个的字母或数字”
    tokeniser = RegexpTokenizer(r'\w+')
    tokens = tokeniser.tokenize(s)
    print(tokens)

    # 词根化
    lemmatiser = WordNetLemmatizer()
    # 获取单词词性
    tagged_sent = pos_tag(tokens)
    lemmas = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas.append(lemmatiser.lemmatize(tag[0], pos=wordnet_pos))
    print(lemmas)

    # 停用词
    keywords = [lemma for lemma in lemmas if lemma not in stopwords.words('english')]
    # print(keywords)

    # 去除纯数字
    nums = [keyword for keyword in keywords if keyword.isdigit()]
    # print(nums)
    letters = [keyword for keyword in keywords if keyword not in nums]
    # print(letters)

    # 大于一个字母的单词才有意义
    word_list = [letter for letter in letters if len(letter) > 1]
    # print(word_list)

    return word_list


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

    # print(items)

    # 输出结果到文件
    fo = open("../output/" + out_file, "w", encoding='UTF-8')
    for item in items:
        fo.write(str(item) + "\n")
    fo.close()


def total_count(str_list):
    """机器学习统计"""
    colname = 'nsdi'

    print("-- Create a dataframe --")
    X_train = pd.DataFrame(str_list, columns=[colname])
    print(X_train)

    # Create an instance of TfidfVectorizer
    vectoriser = TfidfVectorizer(analyzer=preprocessing)
    print("-- Fit to the data and transform to feature matrix --")
    X_train = vectoriser.fit_transform(X_train[colname])
    print(X_train)

    print("-- Convert sparse matrix to dataframe --")
    X_train = pd.DataFrame.sparse.from_spmatrix(X_train)
    print(X_train)

    # Save mapping on which index refers to which words
    col_map = {v: k for k, v in vectoriser.vocabulary_.items()}
    print("--Rename each column using the mapping--")
    for col in X_train.columns:
        X_train.rename(columns={col: col_map[col]}, inplace=True)
    print(X_train)

    # 输出结果到文件
    X_train.to_csv("../output/total.csv")
