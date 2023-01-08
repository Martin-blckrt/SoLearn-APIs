from django.urls import path, include
from .views import PredictionView

app_name = 'presdictions'

urlpatterns = [
    path('prediction', PredictionView.as_view(), name='prediction'),
]