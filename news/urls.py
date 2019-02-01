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

    path('legislation/', views.LegislationList.as_view(), name='legislation'),
    path('legislation/create/', views.LegislationCreate.as_view(), name='legislation-create'),
    path('legislation/<int:pk>/update/', views.LegislationUpdate.as_view(), name='legislation-update'),
    path('legislation/<int:pk>/delete/', views.LegislationDelete.as_view(), name='legislation-delete'),

    path('history/', views.HistoryView.as_view(), name='history'),
    path('director/profile/', views.DirectorProfileView.as_view(), name='director'),
    path('organization/', views.OrganizationChartView.as_view(), name='organization'),
]
