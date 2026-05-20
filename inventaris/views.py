from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
import json
from .models import Barang, Lokasi, FotoBarang
from .forms import BarangForm, LokasiForm, FotoBarangForm
from django.contrib.auth.decorators import login_required


# VIEWS UNTUK BARANG


@login_required
def list_barang(request):
    barang_list = Barang.objects.all().order_by('-tanggal')
    
    # Fitur pencarian berdasarkan nama/deskripsi barang
    search_query = request.GET.get('search', '')
    if search_query:
        barang_list = barang_list.filter(
            Q(nama_barang__icontains=search_query) |
            Q(deskripsi__icontains=search_query)
        )
    
    # Fitur filter berdasarkan kondisi
    kondisi_filter = request.GET.get('kondisi', '')
    if kondisi_filter:
        barang_list = barang_list.filter(kondisi=kondisi_filter)
    
    # Fitur filter berdasarkan lokasi
    lokasi_filter = request.GET.get('lokasi', '')
    if lokasi_filter:
        barang_list = barang_list.filter(lokasi_id=lokasi_filter)
    
    # Ambil semua lokasi untuk dropdown filter
    lokasi_list = Lokasi.objects.all().order_by('nama_lokasi')
    
    # Hitung statistik untuk filter
    total_barang = barang_list.count()
    barang_baik = barang_list.filter(kondisi='baik').count()
    barang_rusak_ringan = barang_list.filter(kondisi='rusak_ringan').count()
    barang_rusak_berat = barang_list.filter(kondisi='rusak_berat').count()
    
    context = {
        'barang_list': barang_list,
        'lokasi_list': lokasi_list,
        'search_query': search_query,
        'kondisi_filter': kondisi_filter,
        'lokasi_filter': lokasi_filter,
        'total_barang': total_barang,
        'barang_baik': barang_baik,
        'barang_rusak_ringan': barang_rusak_ringan,
        'barang_rusak_berat': barang_rusak_berat,
    }
    
    return render(request, 'inventaris/list_barang.html', context)

@login_required
def tambah_barang(request):
    """
    Menambah barang baru beserta upload foto (opsional)
    """
    from .forms import FotoBarangForm
    if request.method == 'POST':
        form = BarangForm(request.POST, request.FILES)
        form_foto = FotoBarangForm(request.POST, request.FILES)
        if form.is_valid():
            barang = form.save()
            # Jika ada file foto, simpan ke FotoBarang
            if request.FILES.get('foto_barang'):
                foto_form = FotoBarangForm(request.POST, request.FILES)
                if foto_form.is_valid():
                    foto = foto_form.save(commit=False)
                    foto.barang = barang
                    foto.save()
            messages.success(request, f'Barang "{barang.nama_barang}" berhasil ditambahkan!')
            return redirect('inventaris:list_barang')
        else:
            messages.error(request, 'Terjadi kesalahan! Silakan periksa data yang dimasukkan.')
            form_foto = FotoBarangForm()
    else:
        form = BarangForm()
        form_foto = FotoBarangForm()
    context = {
        'form': form,
        'form_foto': form_foto,
        'title': 'Tambah Barang Baru'
    }
    return render(request, 'inventaris/tambah_barang.html', context)

@login_required
def edit_barang(request, barang_id):
    """
    Mengedit barang berdasarkan ID
    """
    barang = get_object_or_404(Barang, id=barang_id)
    foto_list = barang.fotos.all()
    if request.method == 'POST':
        form = BarangForm(request.POST, request.FILES, instance=barang)
        if form.is_valid():
            barang = form.save()
            messages.success(request, f'Barang "{barang.nama_barang}" berhasil diperbarui!')
            return redirect('inventaris:list_barang')
        else:
            messages.error(request, 'Terjadi kesalahan! Silakan periksa data yang dimasukkan.')
    else:
        form = BarangForm(instance=barang)
    # Form tambah foto
    from .forms import FotoBarangForm
    form_foto = FotoBarangForm()
    context = {
        'form': form,
        'barang': barang,
        'foto_list': foto_list,
        'form_foto': form_foto,
        'title': 'Edit Barang'
    }
    return render(request, 'inventaris/edit_barang.html', context)

@login_required
def hapus_barang(request, barang_id):
    """
    Menghapus barang berdasarkan ID
    """
    barang = get_object_or_404(Barang, id=barang_id)
    
    if request.method == 'POST':
        nama_barang = barang.nama_barang
        barang.delete()
        messages.success(request, f'Barang "{nama_barang}" berhasil dihapus!')
        return redirect('inventaris:list_barang')
    
    context = {
        'barang': barang,
        'title': 'Hapus Barang'
    }
    
    return render(request, 'inventaris/hapus_barang.html', context)

@login_required
def detail_barang(request, barang_id):
    """
    Menampilkan detail barang dan foto-fotonya, serta form tambah foto
    """
    barang = get_object_or_404(Barang, id=barang_id)
    foto_list = barang.fotos.all()
    if request.method == 'POST':
        form = FotoBarangForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.barang = barang
            foto.save()
            messages.success(request, 'Foto berhasil ditambahkan!')
            return redirect('inventaris:detail_barang', barang_id=barang.id)
    else:
        form = FotoBarangForm()
    context = {
        'barang': barang,
        'foto_list': foto_list,
        'form_foto': form,
        'title': 'Detail Barang'
    }
    return render(request, 'inventaris/detail_barang.html', context)

@login_required
def hapus_foto_barang(request, foto_id):
    """
    Menghapus foto barang berdasarkan ID
    """
    foto = get_object_or_404(FotoBarang, id=foto_id)
    barang_id = foto.barang.id
    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Foto berhasil dihapus!')
    return redirect('inventaris:detail_barang', barang_id=barang_id)

@login_required
def edit_foto_barang(request, foto_id):
    """
    Mengedit foto barang berdasarkan ID
    """
    foto = get_object_or_404(FotoBarang, id=foto_id)
    if request.method == 'POST':
        form = FotoBarangForm(request.POST, request.FILES, instance=foto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto berhasil diupdate!')
            return redirect('inventaris:detail_barang', barang_id=foto.barang.id)
    else:
        form = FotoBarangForm(instance=foto)
    return render(request, 'inventaris/edit_foto_barang.html', {'form': form, 'foto': foto})

#  VIEWS UNTUK LOKASI 

@login_required
def list_lokasi(request):
    """
    Menampilkan daftar semua lokasi
    """
    lokasi_list = Lokasi.objects.all().order_by('nama_lokasi')
    
    # Hitung jumlah barang per lokasi
    for lokasi in lokasi_list:
        lokasi.jumlah_barang = lokasi.barang.count()
    
    context = {
        'lokasi_list': lokasi_list,
    }
    
    return render(request, 'inventaris/list_lokasi.html', context)

@login_required
def tambah_lokasi(request):
    """
    Menambah lokasi baru
    """
    if request.method == 'POST':
        form = LokasiForm(request.POST)
        if form.is_valid():
            lokasi = form.save()
            messages.success(request, f'Lokasi "{lokasi.nama_lokasi}" berhasil ditambahkan!')
            return redirect('inventaris:list_lokasi')
        else:
            messages.error(request, 'Terjadi kesalahan! Silakan periksa data yang dimasukkan.')
    else:
        form = LokasiForm()
    
    context = {
        'form': form,
        'title': 'Tambah Lokasi Baru'
    }
    
    return render(request, 'inventaris/tambah_lokasi.html', context)

@login_required
def edit_lokasi(request, lokasi_id):
    """
    Mengedit lokasi berdasarkan ID
    """
    lokasi = get_object_or_404(Lokasi, id=lokasi_id)
    
    if request.method == 'POST':
        form = LokasiForm(request.POST, instance=lokasi)
        if form.is_valid():
            lokasi = form.save()
            messages.success(request, f'Lokasi "{lokasi.nama_lokasi}" berhasil diperbarui!')
            return redirect('inventaris:list_lokasi')
        else:
            messages.error(request, 'Terjadi kesalahan! Silakan periksa data yang dimasukkan.')
    else:
        form = LokasiForm(instance=lokasi)
    
    context = {
        'form': form,
        'lokasi': lokasi,
        'title': 'Edit Lokasi'
    }
    
    return render(request, 'inventaris/edit_lokasi.html', context)

@login_required
def hapus_lokasi(request, lokasi_id):
    """
    Menghapus lokasi berdasarkan ID
    """
    lokasi = get_object_or_404(Lokasi, id=lokasi_id)
    
    if request.method == 'POST':
        nama_lokasi = lokasi.nama_lokasi
        lokasi.delete()
        messages.success(request, f'Lokasi "{nama_lokasi}" berhasil dihapus!')
        return redirect('inventaris:list_lokasi')
    
    context = {
        'lokasi': lokasi,
        'title': 'Hapus Lokasi'
    }
    
    return render(request, 'inventaris/hapus_lokasi.html', context)

@login_required
def detail_lokasi(request, lokasi_id):
    """
    Menampilkan detail lokasi dan barang yang ada di lokasi tersebut
    """
    lokasi = get_object_or_404(Lokasi, id=lokasi_id)
    barang_list = lokasi.barang.all().order_by('-tanggal')
    
    context = {
        'lokasi': lokasi,
        'barang_list': barang_list,
        'title': 'Detail Lokasi'
    }
    
    return render(request, 'inventaris/detail_lokasi.html', context)

# ===== DASHBOARD VIEW =====

@login_required
def dashboard(request):
    """
    Dashboard monitoring ringkas
    """
    # Hitung total barang
    total_barang = Barang.objects.count()
    
    # Hitung barang berdasarkan kondisi
    barang_baik = Barang.objects.filter(kondisi='baik').count()
    barang_rusak_ringan = Barang.objects.filter(kondisi='rusak_ringan').count()
    barang_rusak_berat = Barang.objects.filter(kondisi='rusak_berat').count()
    
    # Hitung total stok
    total_stok = Barang.objects.aggregate(total=Sum('jumlah'))['total'] or 0
    total_digunakan = Barang.objects.aggregate(total=Sum('digunakan'))['total'] or 0
    total_sisa = total_stok - total_digunakan
    
    # Ambil 5 barang terbaru
    barang_terbaru = Barang.objects.all().order_by('-tanggal')[:5]
    
    # Statistik Barang Masuk per Bulan (khusus dari Jan 2025 sampai bulan ini)
    from datetime import date
    import calendar
    start_year = 2025
    start_month = 1
    today = timezone.now().date()
    chart_labels = []
    chart_data = []
    year = start_year
    month = start_month
    while (year < today.year) or (year == today.year and month <= today.month):
        label = f"{calendar.month_abbr[month]} {year}"
        jumlah = Barang.objects.filter(tanggal__year=year, tanggal__month=month).aggregate(total=Sum('jumlah'))['total'] or 0
        chart_labels.append(label)
        chart_data.append(jumlah)
        # increment month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    
    # Top 3 ruangan dengan barang terbanyak
    top_ruangan_qs = Lokasi.objects.annotate(jumlah_barang=Count('barang')).order_by('-jumlah_barang')[:3]
    top_ruangan = [{'nama': l.nama_lokasi, 'jumlah_barang': l.jumlah_barang} for l in top_ruangan_qs]
    
    # Ringkasan semua barang (nama & stok)
    ringkasan_barang = list(Barang.objects.values('nama_barang', 'sisa'))
    
    # Barang dengan stok menipis (sisa < 10% dari jumlah)
    barang_stok_menipis = [b for b in Barang.objects.all() if b.jumlah > 0 and (b.sisa / b.jumlah) < 0.1]
    
    # Barang rusak
    barang_rusak = Barang.objects.filter(kondisi__in=['rusak_ringan', 'rusak_berat']).order_by('-tanggal')[:5]
    
    # Context
    context = {
        'total_barang': total_barang,
        'barang_baik': barang_baik,
        'barang_rusak_ringan': barang_rusak_ringan,
        'barang_rusak_berat': barang_rusak_berat,
        'total_stok': total_stok,
        'total_digunakan': total_digunakan,
        'total_sisa': total_sisa,
        'barang_terbaru': barang_terbaru,
        'barang_stok_menipis': barang_stok_menipis,
        'barang_rusak': barang_rusak,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'top_ruangan': top_ruangan,
        'ringkasan_barang': ringkasan_barang,
    }
    
    return render(request, 'home/dashboard.html', context)
