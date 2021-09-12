from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _



class Category(TranslatableModel):
    translation = TranslatedFields(
        name=models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Name'))
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'categories/{self.slug}'

class Subcategory(TranslatableModel):
    translation = TranslatedFields(
        name=models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Name'))
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "SubKategoriya"
        verbose_name_plural = "SubKategoriyalar"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'categories/{self.slug}'


class Announcement(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Sarlavha')),
        description=models.TextField(verbose_name=_('Tavsif')))
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, )
    image = models.ImageField(upload_to='elonimages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=12)
    cost = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Elonlar'

    def __str__(self):
        return self.safe_translation_getter('title') or ''

    def get_absolute_url(self):
        return f'blog/{self.slug}'


class PicturesFromTheAnnouncement(models.Model):
    owner = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='picturefromannouncement')
    image = models.ImageField(upload_to='elonrasmlari')

    class Meta:
        verbose_name_plural = 'Pictures from the Announcement'

    def __str__(self):
        return str(self.owner.safe_translation_getter('title')) or ''