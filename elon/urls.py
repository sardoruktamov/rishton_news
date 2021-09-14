from django.urls import path
from .views import AnnouncementList, AnnouncementCreateView, load_category


urlpatterns = [
    path(" ", AnnouncementList.as_view(), name="announcement_list"),
    path('create/', AnnouncementCreateView.as_view(), name="announcement_create"),
    path('ajax/load-subcategory/', load_category, name="ajax_load_subcategory"),
]