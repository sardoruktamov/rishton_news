from django.urls import path
from .views import HomePageView, DetailViews, BlogPageView, CategoriesView

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('blogs/', BlogPageView.as_view(), name="blogpage"),
    path('blog/<str:slug>/', DetailViews.as_view(), name='detailview'),
    path('categories/<str:slug>/', CategoriesView.as_view(), name='categories')
]