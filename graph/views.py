from django.shortcuts import render


def index(request):
    # latest_question_list = []
    latest_question_list = ["question1", "question2"]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'graph/index.html', context)
