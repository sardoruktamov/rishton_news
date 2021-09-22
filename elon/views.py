from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Category, Subcategory, Announcement
from django.urls import reverse_lazy
from .forms import AnnouncementForm

class AnnouncementList(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/announcements.html"

class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/add.html"
    success_url = reverse_lazy('announcement_list')

def load_category(request):
    category_id = request.GET.get('category')
    subcategory = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, "announcement/category_dropdown.html", {'subcategory': subcategory})

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    # template_name = "announcement/add.html"
    success_url = reverse_lazy('announcement_list')