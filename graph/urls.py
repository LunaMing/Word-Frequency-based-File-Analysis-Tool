from django.urls import path

from graph.views import *

urlpatterns = [
    path('', get_index),
    path('getAllAuthors', get_all_authors),
    path('getAllPapers', get_all_papers),
    path('getAllWords', get_all_words),
    path('getAllJson', get_all_json),
    path('getCountJson', get_count_json),
    path('upload', upload),
    path('start', get_new_graph),
]
