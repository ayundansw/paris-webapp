from django.urls import path
from . import views

# Nama app untuk namespace agar url tidak bentrok antar app
app_name = 'inventaris'

urlpatterns = [
    #  DASHBOARD 
    path('', views.dashboard, name='dashboard'),  # Halaman dashboard utama
    
    #  URLS UNTUK BARANG 
    path('barang/', views.list_barang, name='list_barang'),  # Daftar barang
    path('barang/tambah/', views.tambah_barang, name='tambah_barang'),  # Tambah barang
    path('barang/<int:barang_id>/', views.detail_barang, name='detail_barang'),  # Detail barang
    path('barang/<int:barang_id>/edit/', views.edit_barang, name='edit_barang'),  # Edit barang
    path('barang/<int:barang_id>/hapus/', views.hapus_barang, name='hapus_barang'),  # Hapus barang
    
    #  URLS UNTUK FOTO BARANG 
    path('foto/<int:foto_id>/hapus/', views.hapus_foto_barang, name='hapus_foto_barang'),  # Hapus foto barang
    path('foto/<int:foto_id>/edit/', views.edit_foto_barang, name='edit_foto_barang'),  # Edit foto barang

    #  URLS UNTUK LOKASI 
    path('lokasi/', views.list_lokasi, name='list_lokasi'),  # Daftar lokasi
    path('lokasi/tambah/', views.tambah_lokasi, name='tambah_lokasi'),  # Tambah lokasi
    path('lokasi/<int:lokasi_id>/', views.detail_lokasi, name='detail_lokasi'),  # Detail lokasi
    path('lokasi/<int:lokasi_id>/edit/', views.edit_lokasi, name='edit_lokasi'),  # Edit lokasi
    path('lokasi/<int:lokasi_id>/hapus/', views.hapus_lokasi, name='hapus_lokasi'),  # Hapus lokasi
]