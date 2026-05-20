from django import forms
from django.contrib.auth.models import User

# ProfileForm digunakan untuk mengedit profil user (nama, email, keterangan)
class ProfileForm(forms.ModelForm):
    keterangan = forms.CharField(
        label='Keterangan', 
        widget=forms.Textarea(attrs={'rows':3, 'class':'w-full px-3 py-2 border border-gray-300 rounded-md'}), 
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name': 'Nama',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class':'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }
