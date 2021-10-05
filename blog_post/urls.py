from django.urls import path
from .views import (HomePageView, DetailViews,
                    BlogPageView, CategoriesView,
                    tagsfilter, contact, sendmail, Search)

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('blogs/', BlogPageView.as_view(), name="blogpage"),
    path('tagged/<str:name>', tagsfilter, name="tagged_blogs"),
    path('blog/<str:slug>/', DetailViews.as_view(), name='detailview'),
    path('categories/<str:slug>/', CategoriesView.as_view(), name='categories'),
    path('contact/', contact, name='contact'),
    path('search/', Search, name='search'),
    path('sendmail/', sendmail, name="sendmail"),
]