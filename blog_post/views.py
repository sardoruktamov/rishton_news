from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Blog, PicturesFromTheBlog

# Create your views here.
class HomePageView(ListView):
    template_name = 'index.html'
    queryset = Blog.objects.all()[:1]
    # print(queryset.hashtag.all,'999999999999999999999999')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['blog'] = Blog.objects.all()
        return context

class TagListView(ListView):
    """bloglarni taglar yordamida filterlash"""
    template_name = "index.html"

    def get_queryset(self):
        return Blog.objects.filter(hashtag__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        print(context["tag"],'+++++++++++++++++++++++')
        return context

class DetailViews(DetailView):
    model = Blog
    template_name = 'single.html'

    def get_context_data(self, **kwargs):
        context = super(DetailViews, self).get_context_data(**kwargs)
        return context