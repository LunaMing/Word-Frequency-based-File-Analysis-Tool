from django.http import HttpResponse
from django.template import loader


def getIndex(request):
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
