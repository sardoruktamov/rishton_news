from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Category, Subcategory, Announcement
from django.urls import reverse_lazy
from .forms import AnnouncementForm
from django.contrib.auth.mixins import LoginRequiredMixin
from elon.transliterate import to_latin
import json
from django.core import serializers


class AnnouncementList(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/announcements.html"


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/add.html"
    success_url = reverse_lazy('announcement_list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        slug_field = self.request.POST['title']
        if slug_field.isascii():                    # agar kiritilgan malumot isascii jadvalida bolsa pastdagi izox ishlaydi
            self.object.slug = slug_field.replace(" ", "-")  #elon yaratilganda slug maydodidagi bo`sh joylarni "-" bilan almashtirib qoyadi
        else:
            self.object.slug = to_latin(slug_field).replace(" ", "-") # agar kiritilgan malumot isascii jadvalida bol,asa lotin yozuviga aylantiriladi
        return super(AnnouncementCreateView, self).form_valid(form)

class AnnouncementDetailView(DetailView):
    model = Announcement
    context_object_name = 'object'
    template_name = 'announcement/ann_detail.html'

    # def get_queryset(self, request, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     queryset = Announcement.objects.filter(pk=pk)
    #     return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super(AnnouncementDetailView, self).get_context_data(**kwargs)
    #
    #     return context


def add(request):
    categories = Category.objects.all()
    json_serializer = serializers.get_serializer("json")()
    subcategories = json_serializer.serialize(Subcategory.objects.all(), ensure_ascii=False)
    announcements = Announcement.objects.all()

    if request.method == 'POST' and request.FILES:
        image = request.FILES.get('image')
        title = request.POST['title']
        description = request.POST['description']
        category_id = request.POST['category_id']
        subcategory_id = request.POST['subcategory_id']
        full_name = request.POST['full_name']
        address = request.POST['address']
        cost = request.POST['cost']
        phone = request.POST.get('phone', '')

        announcement = Announcement(
            image=image,
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            full_name=full_name,
            address=address,
            cost=cost,
            phone=phone,
        )
        announcement.save()
    return render(request, 'announcement/add.html', {
                      'categories': categories,
                      'subcategories': subcategories,
                      'announcements': announcements,
                  })

def load_category(request):
    category_id = request.GET.get('category_id')
    subcategory = Subcategory.objects.filter(category_id=category_id).all()
    return render(request, "announcement/category_dropdown.html", {'subcategory': subcategory})


class AnnouncementUpdateView(UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    # template_name = "announcement/add.html"
    success_url = reverse_lazy('announcement_list')
