from django.http import JsonResponse

from graph.models import Paper


def getAllPapers(request):
    if request.method == 'GET':
        try:
            papers = Paper.nodes.all()
            response = []
            for paper in papers:
                obj = {
                    "title": paper.title,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
