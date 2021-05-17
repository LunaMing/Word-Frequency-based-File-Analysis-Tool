import os

from django.http import HttpResponse, JsonResponse
from django.template import loader

from algorithm import export_neo4j_data, word_freq, read_pdf_names, import_neo4j, draw_cloud


def get_pdf_pure_name(pdf_path_list):
    pdf_list = []
    for pdf_path in pdf_path_list:
        # res\pdf\nsdi20spring_cheng_prepub_0.pdf
        pdf_name = pdf_path.lstrip("res\\pdf\\")
        pdf_list.append(pdf_name)
    return pdf_list


def get_new_graph(request):
    # 读取pdf文件名
    pdf_path_list = read_pdf_names()
    pdf_list = get_pdf_pure_name(pdf_path_list)

    # 词频统计
    doc_word_list = word_freq(pdf_path_list)

    # 导入数据库
    import_neo4j(pdf_list, doc_word_list)

    # 词云
    cloud_index = 1
    draw_cloud(str(doc_word_list), os.path.join("output", "cloud", str(cloud_index) + ".png"))

    # 图谱
    res = export_neo4j_data()
    node_list = []
    link_list = []
    data_to_node_and_link(res, node_list, link_list)
    template = loader.get_template('graph/index.html')

    context = {
        'pdfs': pdf_list,
        'links': link_list,
        'nodes': node_list,
    }
    return HttpResponse(template.render(context, request))


def data_to_node_and_link(res, node_list, link_list):
    word_set = set()

    node_index = 0

    for paper in res:
        paper_id = node_index
        node_paper = {
            "category": 1,
            "name": paper["title"],
            "symbol": 'rect',
            "value": node_index,
            "symbolSize": [30, 20]
        }
        node_list.append(node_paper)
        node_index += 1

        for author in paper["authors"]:
            author_id = node_index
            node_author = {
                "category": 0,
                "name": author["name"],
                "symbol": 'diamond',
                "value": node_index,
                "symbolSize": 20
            }
            node_list.append(node_author)
            node_index += 1

            link = {
                "source": author_id,
                "target": paper_id
            }
            link_list.append(link)

        for word in paper["words"]:
            word_id = -1
            if word["name"] not in word_set:
                word_set.add(word["name"])
                word_id = node_index
                node_word = {
                    "category": 2,
                    "name": word["name"],
                    "symbol": 'circle',
                    "value": node_index,
                    "symbolSize": 60
                }
                node_list.append(node_word)
                node_index += 1
            else:
                # 如果word已经建立了节点，就查找到这个已经建立过的节点id
                for node in node_list:
                    if node["name"] == word["name"]:
                        word_id = node["value"]
            link = {
                "source": paper_id,
                "target": word_id
            }
            link_list.append(link)
    # 打印调试节点
    # print("--node--")
    # for node in node_list:
    #     print(node)
    # print("--link--")
    # for link in link_list:
    #     print(link)


def get_count_json(r):
    res = [
        {
            "paper": "pdf1",
            "words":
                [
                    {
                        "word": "word1",
                        "num": 55.5
                    },
                    {
                        "word": "word2",
                        "num": 44.4
                    }
                ]
        }
    ]
    return JsonResponse(res, safe=False)
