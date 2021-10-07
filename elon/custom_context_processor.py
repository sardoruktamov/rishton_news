from .models import Announcement, Category

def elon_renderer(request):
    data = {
        'all_announcement':  Announcement.objects.all()
    }
    return data

def ann_category_renderer(request):
    data = {
        'all_ann_category':  Category.objects.all().order_by('slug')
    }
    return data