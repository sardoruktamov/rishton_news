from django.contrib import admin
from .models import Category, Blog, PicturesFromTheBlog, Tags
from parler.admin import TranslatableAdmin


# Register your models here.

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class BlogImageAdmin(admin.StackedInline):
    model = PicturesFromTheBlog

@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
    list_display = ('title', 'category',)
    list_display_links = ('title',)
    search_fields = ['title', 'description', 'category']
    inlines = [BlogImageAdmin]
    # list_filter =

    class Meta:
        model = Blog

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


@admin.register(PicturesFromTheBlog)
class PicturesAdmin(admin.ModelAdmin):  # PicturesAdmin(TranslatableAdmin) bunday qilib yozib bo`lmaydi xatolik beradi
    list_display = ('owner',)



