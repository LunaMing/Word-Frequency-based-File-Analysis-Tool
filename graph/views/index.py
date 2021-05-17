import os

from django.http import HttpResponse, JsonResponse
from django.template import loader

from algorithm import get_all_kind, export_neo4j_data, read_pdf_names
from views import get_pdf_pure_name


def get_index(request):
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


def get_all_papers(r):
    return JsonResponse(get_all_kind('Paper'), safe=False)


def get_all_words(r):
    return JsonResponse(get_all_kind('Word'), safe=False)


def get_all_authors(r):
    return JsonResponse(get_all_kind('Author'), safe=False)


def get_all_json(r):
    return JsonResponse(export_neo4j_data(), safe=False)


def upload(request):
    if request.method == 'POST':  # 获取对象
        obj = request.FILES.get('fafafa')
        # 上传文件的文件名 　　　　
        print(obj.name)
        BASE_DIR = "res"
        f = open(os.path.join(BASE_DIR, 'pdf', obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()

        # 读取pdf文件名
        pdf_path_list = read_pdf_names()
        pdf_list = get_pdf_pure_name(pdf_path_list)
        link_list = []
        node_list = []

        template = loader.get_template('graph/index.html')
        context = {
            'pdfs': pdf_list,
            'links': link_list,
            'nodes': node_list,
        }
        return HttpResponse(template.render(context, request))
