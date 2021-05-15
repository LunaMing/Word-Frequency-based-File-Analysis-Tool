from django.urls import path

from graph.views import *

urlpatterns = [
    path('', getIndex),
    path('getAllAuthors', get_all_authors),
    path('getAllPapers', get_all_papers),
    path('getAllWords', get_all_words),
    path('start', get_new_graph),
    path('getAllJson', get_json_data),
]
