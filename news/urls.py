from django.urls import path
from . import views   

app_name = 'news'

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news_detail/', views.news_detail_view, name='news_detail'),
]

