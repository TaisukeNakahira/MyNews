from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('recommendation', views.recommendation, name='recommendation'),
    path('articles', views.get_articles, name='articles'),
    path('articles_all', views.get_articles_all, name='articles_all'),
    path('create_model_test', views.create_model_test, name='create_model_test'),
    path('create_model', views.create_model, name='create_model'),
    path('morphological_analysis', views.morphological_analysis, name='morphological_analysis'),
]