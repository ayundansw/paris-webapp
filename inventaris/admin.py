from django.contrib import admin

# Register your models here.
from .models import Lokasi, Barang, FotoBarang


# Konfigurasi admin untuk Lokasi

@admin.register(Lokasi)
class LokasiAdmin(admin.ModelAdmin):
    list_display = ['nama_lokasi', 'kode_lokasi', 'jumlah_barang']  # Kolom yang ditampilkan di list
    search_fields = ['nama_lokasi', 'kode_lokasi']  # Kolom pencarian
    ordering = ['nama_lokasi']  # Urutan default
    
    def jumlah_barang(self, obj):
        # Menghitung jumlah barang di lokasi ini
        return obj.barang.count()
    jumlah_barang.short_description = 'Jumlah Barang'


# Konfigurasi admin untuk Barang

@admin.register(Barang)
class BarangAdmin(admin.ModelAdmin):
    list_display = ['nama_barang', 'tanggal', 'jumlah', 'digunakan', 'sisa', 'kondisi', 'lokasi']  # Kolom utama
    list_filter = ['kondisi', 'lokasi', 'tanggal']  # Filter samping
    search_fields = ['nama_barang', 'deskripsi']  # Kolom pencarian
    ordering = ['-tanggal']  # Urutan default
    readonly_fields = ['sisa']  # Field hanya baca
    
    fieldsets = (
        ('Informasi Barang', {
            'fields': ('nama_barang', 'deskripsi', 'tanggal')
        }),
        ('Stok dan Kondisi', {
            'fields': ('jumlah', 'digunakan', 'sisa', 'kondisi')
        }),
        ('Lokasi', {
            'fields': ('lokasi',)
        }),
    )


# Konfigurasi admin untuk FotoBarang

@admin.register(FotoBarang)
class FotoBarangAdmin(admin.ModelAdmin):
    list_display = ['barang', 'foto_barang']  # Kolom utama
    list_filter = ['barang__lokasi']  # Filter berdasarkan lokasi
    search_fields = ['barang__nama_barang']  # Pencarian berdasarkan nama barang