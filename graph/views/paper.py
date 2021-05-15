from django.http import HttpResponse, JsonResponse
from django.template import loader

from graph.models import Paper


def getAllPapers(request):
    try:
        papers = Paper.nodes.all()
        response = []
        for paper in papers:
            obj = {
                "title": paper.title,
            }
            response.append(obj)
        # return JsonResponse(response, safe=False)
    except:
        response = {"error": "Error occurred"}
        return JsonResponse(response, safe=False)

    pdf_list = []
    for paper in papers:
        pdf_list.append(paper.title)

    author_list = ["author1", "author2"]
    title_list = pdf_list
    word_list = ['word1', 'word2', 'word3']

    template = loader.get_template('graph/index.html')
    context = {
        'pdfs': pdf_list,
        'authors': author_list,
        'papers': title_list,
        'words': word_list,
    }
    return HttpResponse(template.render(context, request))
