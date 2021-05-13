from django.urls import path

from graph.views import *
from views.index import index

urlpatterns = [
    path('', index, name='index'),
    path('person', personDetails),
    path('getAllPersons', getAllPersons),
    path('city', cityDetails),
    path('getAllCities', getAllCities),
    path('connectPaC', connectPaC),
    path('connectPaP', connectPaP)
]
