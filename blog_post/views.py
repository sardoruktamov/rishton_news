from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Blog, PicturesFromTheBlog, Tags


# Create your views here.
class HomePageView(ListView):
    template_name = 'index.html'
    queryset = Blog.objects.all()[:1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tags'] = Tags.objects.all()
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
        context['blogs'] = Blog.objects.all()
        return context


class CategoriesView(ListView):
    template_name = 'blog.html'
    model = Blog

    def get_queryset(self):
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset


def tagsfilter(request, id):
    tags = get_object_or_404(Tags, pk=id)
    all_tags = Tags.objects.all()
    nat = Blog.objects.filter(tags=tags)
    context = {
        "object_list": nat,
        "tags": all_tags
    }
    return render(request, "blog.html", context)

# class TagListView(ListView):
#     """bloglarni taglar yordamida filterlash"""
#     template_name = "blog.html"
#
#     def get_queryset(self, id):
#         return Blog.objects.filter(id__slug=self.kwargs.get("id")).all()
#
#     # def get_context_data(self, **kwargs):
#     #     context = super(TagListView, self).get_context_data(**kwargs)
#     #     context["tags"] = self.kwargs.get("name")
#     #     return context
