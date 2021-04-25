from src.pdf2text import pdf2text
from src.word_freq import word_deal, get_cloud, get_text

# crawl()
pdf2text()
s = get_text()
word_deal(s)
get_cloud(s)
