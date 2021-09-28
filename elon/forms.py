from django import forms
from elon.models import Announcement, Subcategory, Category, PicturesFromTheAnnouncement
from parler.forms import TranslatableModelForm
#------for formset----
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

class PicturesFromTheAnnouncementForm(forms.ModelForm):

    class Meta:
        model = PicturesFromTheAnnouncement
        exclude = ()

CollectionTitleFormSet = inlineformset_factory(
    Announcement, PicturesFromTheAnnouncement, form=PicturesFromTheAnnouncementForm,
    fields=['image'], extra=1, can_delete=True
    )

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
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'mahsulot haqida qisqacha ma\'lumot kiriting...(e\'tibor qiling! xaridor birinchi bo\'lib shu qismga e\'tibor qaratadi)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':'5', 'placeholder':'mahsulot haqida to\'liqroq ma\'lumot kiriting...'}),
            'category': forms.Select(
                attrs={'class': 'form-select mb-3', 'aria-label': 'Floating form-select-lg example'}),
            'subcategory': forms.Select(
                attrs={'class': 'form-select mb-3', 'aria-label': 'Floating form-select-lg example'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('title'),
                Field('description'),
                Field('image'),
                Fieldset('Add titles',
                         Formset('titles')),
                Field('category'),
                Field('subcategory'),
                Field('full_name'),
                Field('cost'),
                Field('address'),
                Field('phone'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('translation')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('title')
