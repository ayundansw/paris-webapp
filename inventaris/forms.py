from django import forms
from .models import Lokasi, Barang, FotoBarang


# Form untuk data Lokasi

class LokasiForm(forms.ModelForm):
    class Meta:
        model = Lokasi
        fields = ['nama_lokasi', 'kode_lokasi']
        labels = {
            'nama_lokasi': 'Nama Lokasi',
            'kode_lokasi': 'Kode Lokasi',
        }
        widgets = {
            'nama_lokasi': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Masukkan nama lokasi'
            }),
            'kode_lokasi': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Masukkan kode lokasi'
            }),
        }

    def clean_kode_lokasi(self):
        """
        Validasi custom: kode lokasi minimal 2 karakter dan otomatis kapital.
        """
        kode = self.cleaned_data['kode_lokasi']
        if len(kode) < 2:
            raise forms.ValidationError('Kode lokasi minimal 2 karakter')
        return kode.upper()


# Form untuk data Barang

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = [
            'tanggal', 'nama_barang', 'jumlah', 'kondisi', 'digunakan', 'lokasi', 'deskripsi'
        ]
        labels = {
            'tanggal': 'Tanggal',
            'nama_barang': 'Nama Barang',
            'jumlah': 'Jumlah Stok',
            'kondisi': 'Kondisi',
            'digunakan': 'Jumlah Digunakan',
            'lokasi': 'Lokasi Penyimpanan',
            'deskripsi': 'Deskripsi',
        }
        widgets = {
            'tanggal': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'date'
            }),
            'nama_barang': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Masukkan nama barang'
            }),
            'jumlah': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '0',
                'placeholder': '0'
            }),
            'kondisi': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'digunakan': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '0',
                'placeholder': '0'
            }),
            'lokasi': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Masukkan deskripsi barang (opsional)'
            }),
        }

    def clean(self):
        """
        Validasi bersih untuk memastikan jumlah dan digunakan tidak negatif
        dan digunakan tidak melebihi jumlah.
        """
        cleaned_data = super().clean()
        jumlah = cleaned_data.get('jumlah')
        digunakan = cleaned_data.get('digunakan')
        
        if jumlah is not None and digunakan is not None:
            if digunakan > jumlah:
                raise forms.ValidationError('Jumlah digunakan tidak boleh melebihi jumlah stok')
            if jumlah < 0:
                raise forms.ValidationError('Jumlah stok tidak boleh negatif')
            if digunakan < 0:
                raise forms.ValidationError('Jumlah digunakan tidak boleh negatif')
        
        return cleaned_data


# Form untuk Foto Barang

class FotoBarangForm(forms.ModelForm):
    class Meta:
        model = FotoBarang
        fields = ['foto_barang']
        labels = {
            'foto_barang': 'Foto Barang',
        }
        widgets = {
            'foto_barang': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none',
                'accept': 'image/*',
            }),
        }

    def clean_foto_barang(self):
        """
        Validasi ukuran dan tipe file foto barang.
        """
        foto = self.cleaned_data.get('foto_barang')
        if foto:
            # Validasi ukuran file (max 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file tidak boleh lebih dari 5MB')
            
            # Validasi tipe file
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if foto.content_type not in allowed_types:
                raise forms.ValidationError('Hanya file gambar yang diperbolehkan (JPEG, PNG, GIF)')
        
        return foto
