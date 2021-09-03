from django.urls import path
from .views import HomePageView, TagListView, DetailViews

urlpatterns = [
    path('', HomePageView.as_view()),
    path('blog/<str:slug>/', DetailViews.as_view(), name='detailview'),
    path('tagged/<slug:slug>', TagListView.as_view(), name="tagged_blogs"),
]