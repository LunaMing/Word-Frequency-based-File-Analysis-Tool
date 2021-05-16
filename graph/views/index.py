from django.http import HttpResponse, JsonResponse
from django.template import loader

from algorithm import get_all_kind, export_neo4j_data


def get_index(request):
    pdf_list = []
    link_list = []
    node_list = []

    template = loader.get_template('graph/index.html')
    context = {
        'pdfs': pdf_list,
        'links': link_list,
        'nodes': node_list,
    }
    return HttpResponse(template.render(context, request))


def get_all_papers(r):
    return JsonResponse(get_all_kind('Paper'), safe=False)


def get_all_words(r):
    return JsonResponse(get_all_kind('Word'), safe=False)


def get_all_authors(r):
    return JsonResponse(get_all_kind('Author'), safe=False)


def get_all_json(r):
    return JsonResponse(export_neo4j_data(), safe=False)
