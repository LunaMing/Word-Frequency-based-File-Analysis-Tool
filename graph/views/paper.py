import traceback

from django.http import HttpResponse, JsonResponse
from django.template import loader

from graph.models import Paper


def getAllPapers(request):
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

    for paper in res:
        node_paper = {
            "id": paper["id"],
            "category": 1,
            "name": paper["title"],
            "symbol": 'rect',
            "value": paper["id"],
            "symbolSize": 30
        }
        node_list.append(node_paper)

        for author in paper["authors"]:
            node_author = {
                "id": author["id"],
                "category": 0,
                "name": author["name"],
                "symbol": 'roundRect',
                "value": author["id"],
                "symbolSize": 50
            }
            node_list.append(node_author)
            link = {
                "source": author["id"],
                "target": paper["id"]
            }
            link_list.append(link)

        for word in paper["words"]:
            if word["name"] not in word_set:
                word_set.add(word["name"])
                node_word = {
                    "id": word["id"],
                    "category": 2,
                    "name": word["name"],
                    "symbol": 'circle',
                    "value": word["id"],
                    "symbolSize": 60
                }
                node_list.append(node_word)
            link = {
                "source": paper["id"],
                "target": word["id"]
            }
            link_list.append(link)

    node_list = sorted(node_list, key=lambda e: e.__getitem__('id'))

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
