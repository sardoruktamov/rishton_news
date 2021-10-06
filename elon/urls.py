from django.urls import path
from .views import (
    AnnouncementList, AnnouncementCreateView,
    load_category, AnnouncementDetailView, edit_announcement, delete_announcement, CategoryFilter, SearchAnn
)

urlpatterns = [
    path("", AnnouncementList.as_view(), name="announcement_list"),
    path('create/', AnnouncementCreateView.as_view(), name="announcement_create"),
    path('Announcement/<slug:slug>', AnnouncementDetailView.as_view(), name="ann_detail"),
    path('Announcement/<slug:slug>/update', edit_announcement, name="ann_update"),
    path('Announcement/<slug:slug>/delete', delete_announcement, name="ann_delete"),
    path('categories/<str:slug>', CategoryFilter.as_view(), name="category_filter"),
    path('search/', SearchAnn.as_view(), name="search-ann"),
    path('ajax/load-subcategory/', load_category, name="ajax_load_subcategory"),
]
