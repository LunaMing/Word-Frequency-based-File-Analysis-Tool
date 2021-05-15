import traceback

from django.http import HttpResponse, JsonResponse
from django.template import loader

from graph.models import Paper


def getIndex(request):
    pdf_list = ["nsdi20spring_arashloo_prepub.pdf", "nsdi20spring_birkner_prepub.pdf"]
    link_list = []
    node_list = []

    template = loader.get_template('graph/index.html')
    context = {
        'pdfs': pdf_list,
        'links': link_list,
        'nodes': node_list,
    }
    return HttpResponse(template.render(context, request))
