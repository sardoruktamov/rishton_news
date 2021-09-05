from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Blog, PicturesFromTheBlog

# Create your views here.
class HomePageView(ListView):
    template_name = 'index.html'
    queryset = Blog.objects.all()[:1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['blog'] = Blog.objects.all()
        return context


class DetailViews(DetailView):
    model = Blog
    template_name = 'single.html'

    # def get_queryset(self):
    #     photos = Blog.objects.get(self.kwargs.get("slug"))
    #     return photos

    def get_context_data(self, **kwargs):
        context = super(DetailViews, self).get_context_data(**kwargs)
        return context

class BlogPageView(ListView):
    template_name = 'blog.html'
    queryset = Blog.objects.all()
    context_object_name = 'blogs'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # context['blogs'] = Blog.objects.all()
        return context

class CategoriesView(ListView):
    template_name = 'blog.html'
    model = Blog

    def get_queryset(self):
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset