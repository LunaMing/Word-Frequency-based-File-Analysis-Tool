import pdftotext


def pdf2text():
    # Load your PDF
    with open("../res/pdf/nsdi20spring_arashloo_prepub.pdf", "rb") as f:
        pdf = pdftotext.PDF(f)

    # # If it's password-protected
    # with open("secure.pdf", "rb") as f:
    #     pdf = pdftotext.PDF(f, "secret")

    # How many pages?
    print(len(pdf))

    # Iterate over all the pages
    for page in pdf:
        print(page)

    # Read some individual pages
    print(pdf[0])
    print(pdf[1])

    # Read all the text into one string
    print("\n\n".join(pdf))

    # 打开一个文件
    fo = open("../output/pdf_text.txt", "w", encoding='UTF-8')

    for page in pdf:
        fo.write(str(page) + "\n")

    # 关闭打开的文件
    fo.close()
