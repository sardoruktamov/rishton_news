from django.urls import path
from .views import HomePageView, TagListView, DetailViews, BlogPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('blogs/', BlogPageView.as_view(), name="blogpage"),
    path('blog/<str:slug>/', DetailViews.as_view(), name='detailview'),
    path('tagged/<slug:slug>', TagListView.as_view(), name="tagged_blogs"),
]