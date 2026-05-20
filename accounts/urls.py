from django.urls import path
from . import views

# Routing URL untuk fitur autentikasi user (register, login, logout, profile)
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),  # Halaman registrasi user
    path('login/', views.login_view, name='login'),           # Halaman login user
    path('logout/', views.logout_view, name='logout'),        # Proses logout user
    path('profile/', views.profile_view, name='profile'),     # Halaman profil user
]
