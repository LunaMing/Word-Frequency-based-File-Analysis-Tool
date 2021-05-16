import pandas as pd
import pdftotext
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

from algorithm import cloud


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
    # print(tokens)

    # 词根化
    lemmatiser = WordNetLemmatizer()
    # 获取单词词性
    tagged_sent = pos_tag(tokens)
    lemmas = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas.append(lemmatiser.lemmatize(tag[0], pos=wordnet_pos))
    # print(lemmas)

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
    total_word_num = len(word_list)

    # 统计
    counts = {word: word_list.count(word) for word in set(word_list)}

    # freqs = {word: float(word_list.count(word) / total_word_num) for word in set(word_list)}

    # 排序
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    # 高频阈值：能作为高频候选词的最少出现次数
    LEAST_COUNT = 3
    # 没有超过阈值的不计入高频词候选集
    keys = []
    for item in items:
        if item[1] > LEAST_COUNT:
            keys.append(item)

    key_num = len(keys)

    # 打印topN看一下结果
    top = items[:5]
    print(top)

    # 输出结果到文件
    fo = open("output/" + out_file, "w", encoding='UTF-8')
    fo.write("total word num: " + str(total_word_num) + "\n")
    fo.write("candidate keyword num: " + str(key_num) + "\n")
    for key in keys:
        fo.write(str(key) + "\n")
    fo.close()


def total_count(str_list):
    """机器学习统计"""
    colname = 'nsdi'

    print("-- Create a dataframe --")
    X_train = pd.DataFrame(str_list, columns=[colname])
    print(X_train)

    print("-- Create an instance of TfidfVectorizer --")
    vectoriser = TfidfVectorizer(analyzer=preprocessing)
    print("-- Fit to the data and transform to feature matrix --")
    X_train = vectoriser.fit_transform(X_train[colname])
    print(X_train)

    # print("-- Convert sparse matrix to dataframe --")
    # X_train = pd.DataFrame.sparse.from_spmatrix(X_train)
    # print(X_train)
    #
    # # Save mapping on which index refers to which words
    # col_map = {v: k for k, v in vectoriser.vocabulary_.items()}
    # print("--Rename each column using the mapping--")
    # for col in X_train.columns:
    #     X_train.rename(columns={col: col_map[col]}, inplace=True)
    # print(X_train)

    # # 输出结果到文件
    # X_train.to_csv("output/total.csv")

    return X_train


def word_freq():
    pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub"]

    total_str_list = []
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
        total_str_list.append(s)

    # 统计
    total_count(total_str_list)

    # 词云
    total_str = ""
    for s in total_str_list:
        total_str += s
    cloud.cloud(total_str, "total.png")


if __name__ == '__main__':
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer()
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    X = vectorizer.fit_transform(corpus)
    # print(X)

    analyze = vectorizer.build_analyzer()
    word_bag_list = analyze("This is a text document to analyze.")
    print(word_bag_list)
