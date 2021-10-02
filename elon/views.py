from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Category, Subcategory, Announcement
from django.urls import reverse_lazy, reverse
from .forms import AnnouncementForm
from django.contrib.auth.mixins import LoginRequiredMixin
from elon.transliterate import to_latin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q



class AnnouncementList(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/announcements.html"
    paginate_by = 16

    def get_queryset(self):
        queryset = Announcement.objects.filter(is_public=True)
        return queryset


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/add_and_update.html"
    success_message = "E'loningiz muvoffaqiyatli yaratildi! Bizning xizmatimizdan foydalanganingiz uchun raxmat!"

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
    template_name = "announcement/add_and_update.html"
    success_message = "E'loningiz muvoffaqiyatli o'zgartirildi!"
    success_url = reverse_lazy('announcement_list')

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('ann_detail', kwargs={'slug': self.object.slug})


def edit_announcement(request, slug):
    announ = get_object_or_404(Announcement, slug=slug)
    form = AnnouncementForm(instance=announ)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announ)
        if form.is_valid():
            form.save()
            return render(request, 'announcement/add_and_update.html',
                   {'form': form, 'message': "E'loningiz muvoffaqiyatli o'zgartirildi!"})
    return render(request, 'announcement/add_and_update.html', {'form': form})

def delete_announcement(request, slug):
    elon = get_object_or_404(Announcement, slug=slug)
    if request.method == "POST":
        elon.delete()
        return redirect('announcement_list')


class CategoryFilter(ListView):
    model = Announcement
    template_name = 'announcement/filter.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset