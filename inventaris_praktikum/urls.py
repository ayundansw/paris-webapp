"""
URL configuration for inventaris_praktikum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# =========================
# Django urls.py (root)
# =========================
# Routing utama project, mengarahkan ke app inventaris, accounts, dsb.
# Dokumentasi: https://docs.djangoproject.com/en/4.2/topics/http/urls/
# =========================

urlpatterns = [
    path('admin/', admin.site.urls),
    # Landing page di root path
    path('', lambda request: render(request, 'landing.html'), name='home'),
    # Dashboard dan fitur lain di bawah /dashboard/ dan seterusnya
    path('dashboard/', include('inventaris.urls')),
    path('accounts/', include('accounts.urls')),
]

# Tambahkan static files untuk development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
