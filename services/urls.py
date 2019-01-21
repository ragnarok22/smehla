from django.urls import path

from services import views

app_name = 'services'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('services/status/', views.SearchStatusServiceView.as_view(), name='status'),
    path('tools/', views.ServiceToolsView.as_view(), name='tools'),

    path('client/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('client/list/<type>/', views.ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    path('service/<type>/<int:pk>/add/', views.ServiceCreateView.as_view(), name='service_create'),
    path('service/<str:type>/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('service/<type>/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('service/<str:type>/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    path('service/change/', views.ChangeStatusServiceView.as_view(), name='change_status'),
]
