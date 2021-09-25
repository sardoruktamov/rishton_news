from django.urls import path
from .views import AnnouncementList, AnnouncementCreateView, load_category, add

urlpatterns = [
    path(" ", AnnouncementList.as_view(), name="announcement_list"),
    path('create/', AnnouncementCreateView.as_view(), name="announcement_create"),
    path('add/', add, name="announcement_add"),
    path('ajax/load-subcategory/', load_category, name="ajax_load_subcategory"),
]
