from .models import Category, Blog

def subject_renderer(request):
    data = {
        'all_category':  Category.objects.all()
    }
    return data

#
def blog_processor(request):
    data = {
        'all_blog':  Blog.objects.all()
    }
    return data


