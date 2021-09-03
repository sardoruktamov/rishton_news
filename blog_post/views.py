from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Blog, PicturesFromTheBlog

# Create your views here.
class HomePageView(ListView):
    template_name = 'index.html'
    queryset = Blog.objects.all()[:1]

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        return context