from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('dashboard/', views.DashBoardView.as_view(), name='dashboard'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/detail/', views.ProfileDetailView.as_view(), name='profile_detail'),
]
