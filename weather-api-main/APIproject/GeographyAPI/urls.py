from django.urls import path
from . import views

urlpatterns = [
    path('departements/all', views.DepartementsView.as_view(), name='departements'),
    path('departements/communes/all', views.CommunesView.as_view(), name='communes'),
    path('search/communes', views.SearchSuggestionsView.as_view(), name='searchSuggestions'),
]