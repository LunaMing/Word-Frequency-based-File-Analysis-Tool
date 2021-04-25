from src.picture import cloud
from src.word import word_deal

# crawl()

pdf_name_list = ["nsdi20spring_arashloo_prepub", "nsdi20spring_birkner_prepub"]

for index in range(len(pdf_name_list)):
    pdf_name = pdf_name_list[index]
    s = word_deal(pdf_name)
    cloud(s, pdf_name + ".png")
