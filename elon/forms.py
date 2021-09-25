from django import forms
from elon.models import Announcement, Subcategory
from parler.forms import TranslatableModelForm


class AnnouncementForm(TranslatableModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'description', 'image', 'category', 'subcategory', 'cost', 'full_name', 'address', 'phone',)
        labels = {'title':'Sarlavha',
                  'description':'Tavsif',
                  'image':'Rasm', 'category':'Kategoriya',
                  'subcategory':'Kategoriyaga oid',
                  'cost':'Mahsulot narxi',
                  'full_name':'Ism familya',
                  'address':'Manzil', 'phone':'Telefon'}

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
