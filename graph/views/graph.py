import traceback

from django.http import HttpResponse, JsonResponse
from django.template import loader

from graph.models import Paper


def get_new_graph(request):
    template = loader.get_template('graph/index.html')

    res = get_neo4j_data()
    pdf_list = ["nsdi20spring_arashloo_prepub.pdf", "nsdi20spring_birkner_prepub.pdf"]

    node_list = []

    link_list = []

    data_to_node_and_link(res, node_list, link_list)

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

    print("--node--")
    for node in node_list:
        print(node)
    print("--link--")
    for link in link_list:
        print(link)


def get_json_data(request):
    if request.method == 'GET':
        return JsonResponse(get_neo4j_data(), safe=False)


def get_neo4j_data():
    response = []
    try:
        papers = Paper.nodes.all()
        for paper in papers:
            authors = []
            author_list = paper.get_paper_author()
            for author in author_list:
                author_obj = {
                    "id": author.id,
                    "name": author.name,
                }
                authors.append(author_obj)

            words = []
            word_list = paper.get_contain_words()
            for word in word_list:
                word_obj = {
                    "id": word.id,
                    "name": word.name,
                }
                words.append(word_obj)

            paper = {
                "id": paper.id,
                "title": paper.title,
                "words": words,
                "authors": authors,
            }
            response.append(paper)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {"error": "Error occurred"}
    return response
