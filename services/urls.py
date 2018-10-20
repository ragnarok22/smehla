from django.urls import path

from services import views

app_name = 'services'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('tools/', views.ServiceToolsView.as_view(), name='tools'),
]
