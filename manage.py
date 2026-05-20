#!/usr/bin/env python
# =========================
# Django manage.py
# =========================
# File entry point untuk menjalankan perintah Django (runserver, migrate, dll)
# Tidak perlu diubah kecuali untuk kebutuhan khusus.
#
# Untuk menjalankan server: python manage.py runserver
# Untuk migrasi database: python manage.py migrate
#
# Dokumentasi: https://docs.djangoproject.com/en/4.2/ref/django-admin/
# =========================



import os
import sys


def main():
    """Menjalankan perintah administrasi Django sesuai argumen CLI."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventaris_praktikum.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
