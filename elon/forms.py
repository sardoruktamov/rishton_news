from django import forms
from elon.models import Announcement, Subcategory
from parler.forms import TranslatableModelForm


class AnnouncementForm(TranslatableModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'image', 'image1', 'image2', 'cost', 'category', 'subcategory', 'full_name', 'address', 'phone',)
        labels = {'title':'Sarlavha',
                  'description':'Tavsif',
                  'image':'Rasm-1', 'image1':'Rasm-2(agar mavjud bo\'lsa)', 'image2':'Rasm-3(agar mavjud bo\'lsa)', 'category':'Kategoriya',
                  'subcategory':'Kategoriyaga oid',
                  'cost':'Mahsulot narxi',
                  'full_name':'Ism familya',
                  'address':'Manzil', 'phone':'Telefon'}
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'mahsulot haqida qisqacha ma\'lumot kiriting...(e\'tibor qiling! xaridor birinchi bo\'lib shu qismga e\'tibor qaratadi)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':'5', 'placeholder':'mahsulot haqida to\'liqroq ma\'lumot kiriting...'}),
            'category': forms.Select(
                attrs={'class': 'form-control mb-3', 'aria-label': 'Floating form-select-lg example'}),
            'subcategory': forms.Select(
                attrs={'class': 'form-control mb-3', 'aria-label': 'Floating form-select-lg example'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('translation')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('title')
