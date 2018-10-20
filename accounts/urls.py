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

    path('reset/password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('reset/password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/password/confirm/', views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset/password/complete/', views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
]
