from django.urls import path

from services import views

app_name = 'services'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]
