import wordcloud
from src.word_freq import get_text
w = wordcloud.WordCloud()
s = get_text()
w.generate(s)
w.to_file('../res/output.png')