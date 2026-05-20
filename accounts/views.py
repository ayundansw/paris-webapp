from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm


# View untuk autentikasi user (register, login, logout, profile)


def register_view(request):
    """
    View untuk proses registrasi user baru.
    Jika POST dan data valid, user baru dibuat dan diarahkan ke login.
    Jika username/email sudah dipakai, tampilkan pesan error.
    """
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=nama)
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('accounts:login')
    return render(request, 'accounts/register.html')

def login_view(request):
    """
    View untuk proses login user.
    Jika POST dan data valid, user di-autentikasi dan diarahkan ke dashboard.
    Jika gagal, tampilkan pesan error.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventaris:dashboard')
        else:
            messages.error(request, 'Username atau password salah!')
    return render(request, 'accounts/login.html')

def logout_view(request):
    """
    View untuk logout user. Setelah logout diarahkan ke halaman login.
    """
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """
    View untuk melihat dan mengedit profil user.
    Menampilkan form dengan data user saat ini.
    Jika ada perubahan, simpan dan perbarui data user.
    """
    user = request.user
    # Simpan keterangan di session (atau bisa di model UserProfile jika ingin lebih advance)
    keterangan = request.session.get('keterangan', '')
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        keterangan = request.POST.get('keterangan', '')
        if form.is_valid():
            form.save()
            request.session['keterangan'] = keterangan
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)
    context = {
        'form': form,
        'user': user,
        'keterangan': keterangan
    }
    return render(request, 'accounts/profile.html', context)
