from django.http import HttpResponse
from django.template import loader


def getIndex(request):
    # latest_question_list = []
    latest_question_list = ["question1", "question2"]
    context = {'latest_question_list': latest_question_list}
    template = loader.get_template('graph/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
