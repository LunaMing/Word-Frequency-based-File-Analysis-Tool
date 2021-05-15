from django.urls import path

from graph.views import *

urlpatterns = [
    path('', getIndex),
    path('getAllAuthors', getAllAuthors),
    path('getAllPapers', getAllPapers),
    path('getAllJson', get_json_data),
]
