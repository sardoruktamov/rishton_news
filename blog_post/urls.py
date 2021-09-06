from django.urls import path
from .views import HomePageView, DetailViews, BlogPageView, CategoriesView, tagsfilter

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('blogs/', BlogPageView.as_view(), name="blogpage"),
    path('tagged/<int:id>', tagsfilter, name="tagged_blogs"),
    path('blog/<str:slug>/', DetailViews.as_view(), name='detailview'),
    path('categories/<str:slug>/', CategoriesView.as_view(), name='categories')
]