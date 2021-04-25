from src.picture import get_cloud
from src.word import pdf2text, get_text, word_deal

# crawl()
pdf2text()
s = get_text()
word_deal(s)
get_cloud(s)
