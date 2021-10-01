from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Category, Subcategory, Announcement
from django.urls import reverse_lazy, reverse
from .forms import AnnouncementForm
from django.contrib.auth.mixins import LoginRequiredMixin
from elon.transliterate import to_latin
from django.contrib.messages.views import SuccessMessageMixin
import json
from django.core import serializers


class AnnouncementList(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/announcements.html"


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/add.html"
    success_message = "E'loningiz muvoffaqiyatli yaratildi, Bizning xizmatimizdan foydalanganingiz uchun raxmat!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        slug_field = self.request.POST['title']
        if slug_field.isascii():  # agar kiritilgan malumot isascii jadvalida bolsa pastdagi izox ishlaydi
            self.object.slug = slug_field.replace(" ",
                                                  "-")  # elon yaratilganda slug maydodidagi bo`sh joylarni "-" bilan almashtirib qoyadi
        else:
            self.object.slug = to_latin(slug_field).replace(" ",
                                                            "-")  # agar kiritilgan malumot isascii jadvalida bol,asa lotin yozuviga aylantiriladi
        return super(AnnouncementCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        print(self.object.slug,'+++++++++++++++++++++++++')
        return reverse_lazy('ann_detail', kwargs={'slug': self.object.slug})


class AnnouncementDetailView(DetailView):
    model = Announcement
    context_object_name = 'object'
    template_name = 'announcement/ann_detail.html'


def load_category(request):
    category_id = request.GET.get('category_id')
    subcategory = Subcategory.objects.filter(category_id=category_id).all()
    return render(request, "announcement/category_dropdown.html", {'subcategory': subcategory})


class AnnouncementUpdateView(SuccessMessageMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/ann_update.html"
    success_message = "E'loningiz muvoffaqiyatli o'zgartirildi!"
    # success_url = reverse_lazy('announcement_list')

    def get_success_url(self, **kwargs):
        return reverse("ann_update")


def edit_announcement(request, slug):
    person = get_object_or_404(Announcement, slug=slug)
    form = AnnouncementForm(instance=person)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            render(request, 'announcement/add.html',
                   {'form': form, 'message': "E'loningiz muvoffaqiyatli o'zgartirildi!"})
    return render(request, 'announcement/add.html', {'form': form, 'message': "E'loningiz muvoffaqiyatli o'zgartirildi!"})

# def edit_announcement(request, id):
#     elon = get_object_or_404(Announcement, pk=id)
#     form = AnnouncementForm(instance=elon)
#     print(elon,'++++++++++++++++')
#     if request.method == 'POST':
#
#         form = AnnouncementForm(request.POST, request.FILES, instance=elon)
#
#         if form.is_valid():
#             form.save()
#             return redirect('/elonlar/')
#     context = {'form': form}
#     return render(request, 'announcement/ann_update.html', context)

# def edit_announcement(request, slug):
#     post = Announcement.objects.get(slug=slug)
#     print(post,'+++++++++++++++++++')
#     if request.method == "POST":
#         form = AnnouncementForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.tags.update()
#             post.save()
#             return redirect("edit_post", slug=post.slug)
#         else:
#             form = AnnouncementForm(instance=post)
#     form = AnnouncementForm(instance=post)
#     print(form,'-------------------------------')
#     return render(request, 'announcement/ann_update.html', context={'form': form, "post": post})
