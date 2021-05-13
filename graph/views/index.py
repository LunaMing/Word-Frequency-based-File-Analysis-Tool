from django.http import HttpResponse
from django.template import loader


def getIndex(request):
    latest_question_list = ["author-0", "author-1"]
    title_list = ['Frequency Configuration for Low-Power Wide-Area Networks in a Heartbeat',
                  'Plankton: Scalable network configuration verification through model checking']
    template = loader.get_template('graph/index.html')
    context = {
        'author_0': latest_question_list[0],
        'author_1': latest_question_list[1],
        'title_0': title_list[0],
        'title_1': title_list[1],
    }
    return HttpResponse(template.render(context, request))
