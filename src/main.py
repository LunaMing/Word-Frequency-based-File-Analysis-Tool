from src.picture import cloud
from src.word import word_deal

# crawl()

pdf_name = "nsdi20spring_arashloo_prepub"
s = word_deal(pdf_name)
cloud(s, "arashloo.png")

pdf_name = "nsdi20spring_birkner_prepub"
s = word_deal(pdf_name)
cloud(s, "birkner.png")
