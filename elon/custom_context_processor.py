from .models import Announcement, Category
from datetime import datetime


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

def ann_date(request):

    now = datetime.now()
    print(now,'+++++++++++++++++++++')
    return now