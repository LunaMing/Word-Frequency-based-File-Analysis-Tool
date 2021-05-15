from django.urls import path

from graph.views import *

urlpatterns = [
    path('', getIndex),
    path('getAllAuthors', getAllAuthors),
    path('getAllPapers', getAllPapers),
    path('start', get_new_graph),
    path('getAllJson', get_json_data),
]
