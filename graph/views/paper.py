import traceback

from django.http import HttpResponse, JsonResponse
from django.template import loader

from graph.models import Paper


def getAllPapers(request):
    pdf_list = []
    try:
        papers = Paper.nodes.all()
        response = []
        for paper in papers:
            pdf_list.append(paper.title)
            word_list = paper.get_contain_words()
            word_name_list = []
            for word in word_list:
                word_id = word.id
                word_name = word.name
                word_obj = {
                    "id": word_id,
                    "name": word_name
                }
                word_name_list.append(word_obj)
            obj = {
                "id": paper.id,
                "title": paper.title,
                "words": word_name_list
            }
            response.append(obj)
    except Exception as e:
        print(e)
        traceback.print_exc()
        response = {"error": "Error occurred"}
        return JsonResponse(response, safe=False)

    template = loader.get_template('graph/index.html')

    author_list = ["Mina Tahmasbi Arashloo", "Rüdiger Birkner"]
    paper_list = [
        'Enabling Programmable Transport Protocols in High-Speed NICs',
        'Config2Spec: Mining Network Specifications from Network Configurations'
    ]
    word_list = ["machine learning", "flow"]
    node_list = []
    node_author = {
        "id": 0,
        "category": 0,
        "name": author_list[0],
        "symbol": 'roundRect',
        "value": 20,
        "symbolSize": 50
    }
    node_list.append(node_author)
    node_paper = {
        "id": 1,
        "category": 1,
        "name": paper_list[0],
        "symbol": 'rect',
        "value": 20,
        "symbolSize": 30
    }
    node_list.append(node_paper)
    node_word = {
        "id": 2,
        "category": 2,
        "name": word_list[0],
        "symbol": 'circle',
        "value": 20,
        "symbolSize": 60
    }
    node_list.append(node_word)

    link_list = [{"source": 0, "target": 1}, {"source": 1, "target": 2}]

    context = {
        'pdfs': pdf_list,
        'links': link_list,
        'nodes': node_list,
    }
    return HttpResponse(template.render(context, request))


def getAllContainWords(request):
    if request.method == 'GET':
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
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
