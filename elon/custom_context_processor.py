from .models import Announcement

def elon_renderer(request):
    data = {
        'all_announcement':  Announcement.objects.all()[:1]
    }
    return data
