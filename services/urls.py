from django.urls import path

from services import views

app_name = 'services'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('tools/', views.ServiceToolsView.as_view(), name='tools'),

    path('client/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('client/list/', views.ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    path('visa/add/', views.VisaCreateView.as_view(), name='visa_create'),
    path('visa/list/', views.VisaListView.as_view(), name='visa_list'),
    path('visa/<int:pk>/detail/', views.VisaDetailView.as_view(), name='visa_detail'),
    path('visa/<int:pk>/update/', views.VisaUpdateView.as_view(), name='visa_update'),
    path('visa/<int:pk>/delete/', views.VisaDeleteView.as_view(), name='visa_delete'),
]
