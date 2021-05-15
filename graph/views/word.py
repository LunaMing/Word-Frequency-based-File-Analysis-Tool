from django.http import JsonResponse

from graph.models import Word


def getAllWords(request):
    if request.method == 'GET':
        try:
            words = Word.nodes.all()
            response = []
            for word in words:
                obj = {
                    "name": word.name,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)