from django.urls import path

from news import views

app_name = 'news'
urlpatterns = [
    path('create/', views.NewsCreateView.as_view(), name='create'),
    path('', views.NewsListView.as_view(), name='list'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/', views.NewsDetailView.as_view(), name='detail'),

    path('services/', views.ServiceList.as_view(), name='services'),
    path('services/create/', views.ServiceCreate.as_view(), name='service-create'),
    path('services/<int:pk>/update/', views.ServiceUpdate.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', views.ServiceDelete.as_view(), name='service-delete'),
]
