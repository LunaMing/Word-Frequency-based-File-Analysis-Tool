from django.http import JsonResponse

from graph.models import Author


def getAllAuthors(request):
    if request.method == 'GET':
        try:
            authors = Author.nodes.all()
            response = []
            for author in authors:
                obj = {
                    "name": author.name,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
