import traceback

from django.http import JsonResponse

from graph.models import Author, Paper, Word


def get_all_kind(kind, request):
    if request.method == 'GET':
        try:
            if kind == 'Paper':
                nodes = Paper.nodes.all()
            elif kind == 'Author':
                nodes = Author.nodes.all()
            elif kind == 'Word':
                nodes = Word.nodes.all()
            else:
                raise Exception("'kind' not in Paper or Author or Word")
            response = []
            for node in nodes:
                if kind == 'Paper':
                    obj = node.title
                elif kind == 'Author' or 'Word':
                    obj = node.name
                else:
                    raise Exception("'kind' not in Paper or Author or Word")
                response.append(obj)
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            traceback.print_exc()
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)


def get_all_papers(request):
    return get_all_kind('Paper', request)


def get_all_words(request):
    return get_all_kind('Word', request)


def get_all_authors(request):
    return get_all_kind('Author', request)
