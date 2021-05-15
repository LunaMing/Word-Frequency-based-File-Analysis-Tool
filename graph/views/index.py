from django.http import HttpResponse
from django.template import loader


def getIndex(request):
    pdf_list = ["nsdi20spring_arashloo_prepub.pdf", "nsdi20spring_birkner_prepub.pdf"]
    author_list = ["Mina Tahmasbi Arashloo", "Rüdiger Birkner"]
    title_list = [
        'Enabling Programmable Transport Protocols in High-Speed NICs',
        'Config2Spec: Mining Network Specifications from Network Configurations'
    ]
    word_list = ['segment', 'tonic', 'flow']

    template = loader.get_template('graph/index.html')
    context = {
        'pdfs': pdf_list,
        'authors': author_list,
        'papers': title_list,
        'words': word_list,
    }
    return HttpResponse(template.render(context, request))
