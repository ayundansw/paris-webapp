from django.apps import AppConfig


# Konfigurasi AppConfig untuk aplikasi inventaris

class InventarisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Tipe primary key default
    name = 'inventaris'  # Nama app
