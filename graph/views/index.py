import os
import shutil

from django.http import HttpResponse, JsonResponse
from django.template import loader

from algorithm import get_all_kind, export_neo4j_data, read_pdf_names
from views import get_pdf_pure_name


def setDir(filepath):
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    :param filepath:需要创建的文件夹路径
    :return:
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


def get_index(request):
    # 清空pdf文件夹数据
    setDir(os.path.join("res", "pdf"))
    # 清空数据库数据

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
        if obj is not None:
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
