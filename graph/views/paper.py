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
            word_list = paper.contain_words()
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
    author_list = ["author1", "author2"]
    title_list = pdf_list
    word_list = ['word1', 'word2', 'word3']
    link_list = []
    for item in response:
        paper_id = item["id"]
        for word in item["words"]:
            word_id = word["id"]
            onelink = {
                "source": paper_id,
                "target": word_id
            }
            link_list.append(onelink)

    template = loader.get_template('graph/index.html')

    link_list = [{"source": 0, "target": 1}]

    # [
    #                         {
    #                             id: 0,
    #                             category: 0,
    #                             name: author_list[0],
    #                             symbol: 'roundRect',
    #                             value: 20,
    #                             symbolSize: 50,
    #                         }, {
    #                             id: 1,
    #                             category: 1,
    #                             name: paper_list[0],
    #                             symbol: 'rect',
    #                             value: 20,
    #                             symbolSize: 30,
    #                         }, {
    #                             id: 2,
    #                             category: 1,
    #                             name: paper_list[1],
    #                             symbol: 'rect',
    #                             value: 20,
    #                             symbolSize: 70
    #                         }, {
    #                             id: 3,
    #                             category: 2,
    #                             name: word_list[0],
    #                             symbol: 'circle',
    #                             value: 20,
    #                             symbolSize: 60
    #                         }, {
    #                             id: 4,
    #                             category: 2,
    #                             name: word_list[1],
    #                             symbol: 'circle',
    #                             value: 20,
    #                             symbolSize: 60
    #                         }]
    author_list = ["Mina Tahmasbi Arashloo", "Rüdiger Birkner"]
    paper_list = [
        'Enabling Programmable Transport Protocols in High-Speed NICs',
        'Config2Spec: Mining Network Specifications from Network Configurations'
    ]
    node_list = []
    onenode = {
        "id": 0,
        "category": 0,
        "name": author_list[0],
        "symbol": 'roundRect',
        "value": 20,
        "symbolSize": 50
    }
    node_list.append(onenode)
    twonode = {
        "id": 1,
        "category": 1,
        "name": paper_list[0],
        "symbol": 'rect',
        "value": 20,
        "symbolSize": 30
    }
    node_list.append(twonode)

    context = {
        'pdfs': pdf_list,
        'authors': author_list,
        'papers': title_list,
        'words': word_list,
        'links': link_list,
        'nodes': node_list,
    }
    return HttpResponse(template.render(context, request))


def getAllContainWords(request):
    if request.method == 'GET':
        try:
            papers = Paper.nodes.all()
            response = []
            for paper in papers:
                word_list = paper.contain_words()
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
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
