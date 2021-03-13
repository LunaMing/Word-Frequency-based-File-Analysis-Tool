from nltk.corpus import stopwords


def getText():
    txt = open('raw.txt', 'r', encoding='UTF-8').read()

    txt = txt.lower()
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
        txt = txt.replace(ch, " ")  # 将文本中特殊字符替换为空格
    for ch in '0123456789':
        txt = txt.replace(ch, " ")  # 将文本中数字替换为空格
    return txt


hamletTxt = getText()
words = hamletTxt.split()

# 停用词表
word_list = []
for word in words:
    word_list.append(word)

filtered_words = [word for word in word_list if word not in stopwords.words('english')]


counts = {}
for word in filtered_words:
    counts[word] = counts.get(word, 0) + 1
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)
for i in range(10):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count))

# 打开一个文件
fo = open("word_result.txt", "w", encoding='UTF-8')

for item in items:
    fo.write(str(item) + "\n")

# 关闭打开的文件
fo.close()
