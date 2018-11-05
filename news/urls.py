from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('create/', views.NewsCreateView.as_view(), name='create'),
    path('', views.NewsListView.as_view(), name='list'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/', views.NewsDetailView.as_view(), name='detail'),
]
