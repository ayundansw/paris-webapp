from .models import Barang, Lokasi

def sidebar_data(request):
    """
    Context processor untuk menambahkan data statistik sidebar ke semua template.
    Mengembalikan total barang dan total lokasi.
    """
    try:
        total_barang = Barang.objects.count()  # Hitung total barang
        total_lokasi = Lokasi.objects.count()  # Hitung total lokasi
    except:
        # Jika database belum siap, gunakan nilai default
        total_barang = 0
        total_lokasi = 0
    return {
        'sidebar_total_barang': total_barang,
        'sidebar_total_lokasi': total_lokasi,
    }