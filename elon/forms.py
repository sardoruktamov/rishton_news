from django import forms
from elon.models import Announcement, Subcategory
from parler.forms import TranslatableModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class AnnouncementForm(TranslatableModelForm):
    class Meta:
        model = Announcement
        fields = (
            'title', 'description', 'image', 'image1', 'image2', 'cost', 'category', 'subcategory',
            'full_name', 'address', 'phone',)
        labels = {'title': 'Sarlavha',
                  'description': 'Tavsif',
                  'image': 'Rasm-1', 'image1': 'Rasm-2(agar mavjud bo\'lsa)', 'image2': 'Rasm-3(agar mavjud bo\'lsa)',
                  'category': 'Kategoriya',
                  'subcategory': 'Kategoriyaga oid',
                  'cost': 'Mahsulot narxi',
                  'full_name': 'Ism familya',
                  'address': 'Manzil', 'phone': 'Telefon'}
        widgets = {
            # 'image': forms.FileInput(attrs={'class': 'form-control'}),
            # 'image1': forms.FileInput(attrs={'class': 'form-control'}),
            # 'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'mahsulot haqida qisqacha ma\'lumot kiriting...(e\'tibor qiling! xaridor birinchi bo\'lib shu qismga e\'tibor qaratadi)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '6',
                                                 'placeholder': 'mahsulot haqida to\'liqroq ma\'lumot kiriting...'}),
            'category': forms.Select(
                attrs={'class': 'form-control mb-3', 'aria-label': 'Floating form-select-lg example'}),
            'subcategory': forms.Select(
                attrs={'class': 'form-control mb-3', 'aria-label': 'Floating form-select-lg example'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'so\'mda, $ yoki ayriboshlash kabi ma\'lumotlar ham kiriting'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by(
                    'translation')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('translation')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ismingizni kiriting', 'required': True, 'autofocus': True}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Elektron pochtangizni kiriting...', 'required': True, 'autofocus': True}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Parolni kiriting..', 'required': True, 'autofocus': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Parolni takrorlang...', 'required': True, 'autofocus': True}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form__input', 'id':'username','name':'username', 'placeholder': 'Username', 'required': True, 'autofocus': True}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form__input', 'id':'password', 'placeholder': 'Password', 'required': True}))
    remember_me = forms.BooleanField(required=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'username': 'Login', 'first_name': 'Ism', 'last_name': 'Familya', 'email': 'Elektron pochta'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
