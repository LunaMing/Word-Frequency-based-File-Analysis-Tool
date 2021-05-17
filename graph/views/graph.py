import os

from django.http import HttpResponse, JsonResponse
from django.template import loader

from algorithm import export_neo4j_data, word_freq, read_pdf_names, import_neo4j, draw_cloud, read_text


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

    # pdf 小于3个文件 不进入统计函数
    if len(pdf_path_list) < 3:
        return JsonResponse({
            "msg": "The number of PDF files is less than 3,"
                   " and the word frequency analysis of the conference as a whole cannot be performed."
                   " Please continue to upload your paper files."},
            safe=False)

    pdf_list = get_pdf_pure_name(pdf_path_list)
    # 拼凑obj
    pdf_obj_list = []
    i = 0
    for pdf_name in pdf_list:
        i += 1
        pdf = {
            "index": i,
            "name": pdf_name
        }
        pdf_obj_list.append(pdf)

    # 词频统计
    doc_word_list = word_freq(pdf_path_list)

    # 导入数据库
    import_neo4j(pdf_list, doc_word_list)

    # 词云
    cloud_obj_list = []
    cloud_str_list = read_text(pdf_path_list)
    for i in range(len(pdf_path_list)):
        cloud_str = cloud_str_list[i]
        cloud_path = os.path.join("graph", "images", "cloud", str(i) + ".png")
        cloud_draw_path = os.path.join("static", cloud_path)
        draw_cloud(cloud_str, cloud_draw_path)
        obj = {
            "path": cloud_path,
            "index": i + 1
        }
        cloud_obj_list.append(obj)

    # 图谱
    res = export_neo4j_data()
    node_list = []
    link_list = []
    data_to_node_and_link(res, node_list, link_list)
    template = loader.get_template('graph/index.html')

    context = {
        'pdfs': pdf_obj_list,
        'links': link_list,
        'nodes': node_list,
        'clouds': cloud_obj_list,
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
            "symbol": 'diamond',
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
