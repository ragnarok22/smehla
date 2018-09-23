from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<int:pk>/detail/', views.ProfileDetailView.as_view(), name='profile_detail'),
    # path('login/', views.LoginView.as_view(), name='login'),
]
