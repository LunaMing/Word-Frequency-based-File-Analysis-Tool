from django.http import HttpResponse
from django.template import loader


def getIndex(request):
    # edges代表节点间的关系数据。
    edges = '[{source:1,target:0},{source:1,target:3},{source:1,target:4}]'
    author_list = ["Mina Tahmasbi Arashloo", "Rüdiger Birkner"]
    title_list = ['Enabling Programmable Transport Protocols in High-Speed NICs',
                  'Config2Spec: Mining Network Specifications from Network Configurations']
    word_list = ['segment', 'tonic', 'flow']

    template = loader.get_template('graph/index.html')
    context = {
        'author_0': author_list[0],
        'author_1': author_list[1],
        'title_0': title_list[0],
        'title_1': title_list[1],
        'edges': edges,
        'word_0':word_list[0],
        'word_1': word_list[1],
    }
    return HttpResponse(template.render(context, request))
