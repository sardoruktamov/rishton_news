from django.contrib import admin
from .models import Category, Blog, PicturesFromTheBlog
from parler.admin import TranslatableAdmin
# Register your models here.

@admin.register(Category)
class RegiosnsAdmin(TranslatableAdmin):
    list_display = ('name',)

@admin.register(Blog)
class RegiosnsAdmin(TranslatableAdmin):
    list_display = ('title', 'category',)
    list_display_links = ('title',)

@admin.register(PicturesFromTheBlog)
class RegiosnsAdmin(TranslatableAdmin):
    list_display = ('owner',)