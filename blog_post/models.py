
from django.db import models
from taggit.managers import TaggableManager
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


class Blog(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_('Title')),
        description=models.TextField(verbose_name=_('Description')))
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    image = models.ImageField(upload_to='blogimages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    hashtag = TaggableManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.safe_translation_getter('title') or ''

    def get_absolute_url(self):
        return f'blog/{self.slug}'

class PicturesFromTheBlog(models.Model):
    owner = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='picturefromblog')
    image = models.ImageField(upload_to='shotsinblogs')

    class Meta:
        verbose_name_plural = 'Pictures from the blog'

    def __str__(self):
        return str(self.owner.safe_translation_getter('title')) or ''