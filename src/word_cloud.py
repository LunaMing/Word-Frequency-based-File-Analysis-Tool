import wordcloud

from src.word_freq import get_text


def get_cloud():
    w = wordcloud.WordCloud(background_color='white')
    s = get_text()
    w.generate(s)
    w.to_file('../res/output.png')