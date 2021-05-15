from django.http import HttpResponse
from django.template import loader

from algorithm import word_freq
from views.controller import export_neo4j_data


def get_new_graph(request):
    # 读取文件名
    pdf_list = ["nsdi20spring_arashloo_prepub.pdf", "nsdi20spring_birkner_prepub.pdf"]
    # 词频统计
    word_freq()
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
