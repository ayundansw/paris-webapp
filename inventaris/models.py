from django.db import models
from django.core.exceptions import ValidationError

# Model untuk data Lokasi
class Lokasi(models.Model):
    nama_lokasi = models.CharField(max_length=100)  # Nama lokasi ruangan
    kode_lokasi = models.CharField(max_length=10, unique=True)  # Kode unik lokasi

    def __str__(self):
        # Tampilkan nama lokasi pada representasi string
        return self.nama_lokasi

    class Meta:
        verbose_name = "Lokasi"
        verbose_name_plural = "Lokasi"


# Model untuk data Barang

class Barang(models.Model):
    tanggal = models.DateField()  # Tanggal pencatatan barang
    nama_barang = models.CharField(max_length=255)  # Nama barang
    jumlah = models.IntegerField()  # Jumlah stok barang
    kondisi_choices = [
        ('baik', 'Baik'),
        ('rusak_ringan', 'Rusak Ringan'),
        ('rusak_berat', 'Rusak Berat'),
    ]
    kondisi = models.CharField(max_length=20, choices=kondisi_choices, default='baik')  # Kondisi barang
    digunakan = models.IntegerField()  # Jumlah barang yang digunakan
    lokasi = models.ForeignKey(Lokasi, on_delete=models.CASCADE, related_name='barang')  # Lokasi penyimpanan
    deskripsi = models.TextField(blank=True, null=True)  # Keterangan tambahan
    sisa = models.IntegerField(editable=False)  # Stok tersisa (otomatis, tidak bisa diedit manual)

    def __str__(self):
        # Tampilkan nama barang pada representasi string
        return self.nama_barang

    def clean(self):
        """
        Validasi custom untuk memastikan jumlah digunakan dan stok valid.
        """
        if self.digunakan > self.jumlah:
            raise ValidationError('Jumlah digunakan tidak boleh melebihi jumlah stok')
        if self.digunakan < 0:
            raise ValidationError('Jumlah digunakan tidak boleh negatif')
        if self.jumlah < 0:
            raise ValidationError('Jumlah stok tidak boleh negatif')

    def save(self, *args, **kwargs):
        """
        Override save untuk menghitung sisa stok otomatis sebelum menyimpan.
        """
        # Set default value untuk digunakan jika kosong
        if not hasattr(self, 'digunakan') or self.digunakan is None:
            self.digunakan = 0
        # Hitung sisa stok
        self.sisa = self.jumlah - self.digunakan
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Barang"
        verbose_name_plural = "Barang"


# Model untuk Foto Barang

class FotoBarang(models.Model):
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE, related_name='fotos')  # Relasi ke barang
    foto_barang = models.ImageField(upload_to="foto_barang/", blank=True, null=True)  # File foto barang

    def __str__(self):
        if self.barang:
            return f"Foto {self.barang.nama_barang}"
        return "Foto Unknown"

    class Meta:
        verbose_name = "Foto Barang"
        verbose_name_plural = "Foto Barang"