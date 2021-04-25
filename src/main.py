from src.picture import get_cloud
from src.word import pdf2text, get_text, word_deal

# crawl()
pdf2text("nsdi20spring_arashloo_prepub.pdf", "pdf_text.txt")
s = get_text("pdf_text.txt")
word_deal(s)
s = get_text("raw.txt")
get_cloud(s)
