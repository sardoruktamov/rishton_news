from .models import Category, Blog

def subject_renderer(request):
    data = {
        'all_category':  Category.objects.all()
    }
    return data


def blog_processor(request):
    data = {
        'all_blog':  Blog.objects.all()[1:5]
    }
    return data

def blog_content(request):
    data = {
        'all_blog_content':  Blog.objects.all()
    }
    return data
