from django.contrib import admin
from .models import Category, Subcategory, Announcement, PicturesFromTheAnnouncement
from parler.admin import TranslatableAdmin


# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name','image',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(Subcategory)
class SubcategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'category',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class AnnouncementImageAdmin(admin.TabularInline):
    model = PicturesFromTheAnnouncement

@admin.register(Announcement)
class Announcementdmin(TranslatableAdmin):
    list_display = ('title', 'description', 'category', 'is_public')
    list_editable = ('is_public',)
    list_display_links = ('title',)
    search_fields = ['title', 'description', 'category']
    inlines = [AnnouncementImageAdmin]
    list_filter = ('category', 'created_at')
    save_on_top = True  # saqlash va o`chirish tugmalarini sahifa yuqorisiga ham qo`shimcha sifatida olib chiqish uchun
    save_as = True

    class Meta:
        model = Announcement

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


@admin.register(PicturesFromTheAnnouncement)
class AnnouncementPicturesAdmin(admin.ModelAdmin):  # PicturesAdmin(TranslatableAdmin) bunday qilib yozib bo`lmaydi xatolik beradi
    list_display = ('owner',)



