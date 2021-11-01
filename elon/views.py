from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, RedirectView
from .models import Category, Subcategory, Announcement
from django.urls import reverse_lazy, reverse
from .forms import AnnouncementForm, SignUpForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from elon.transliterate import to_latin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.db.models import Q
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout as auth_logout
from datetime import datetime


#elonlar royxati
class AnnouncementList(ListView):
    model = Announcement
    context_object_name = "announcement"
    template_name = "announcement/announcements.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = Announcement.objects.filter(is_public=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context

#elpn yaratish
class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcement/add_and_update.html"
    login_url = 'login'
    success_message = "E'loningiz muvoffaqiyatli yaratildi! Bizning xizmatimizdan foydalanganingiz uchun raxmat!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save(commit=False)
        slug_field = self.request.POST['title']
        if slug_field.isascii():  # agar kiritilgan malumot isascii jadvalida bolsa pastdagi izox ishlaydi
            self.object.slug = slug_field.replace(" ",
                                                  "-").replace(".",
                                                               "-").replace("'",
                                                                         "-")  # elon yaratilganda slug maydonidagi
            # bo`sh joylarni va nuqtani "-" bilan almashtirib qoyadi
        else:
            self.object.slug = to_latin(slug_field).replace(" ",
                                                            "-").replace(".",
                                                                         "-").replace("ь",
                                                                         "-")  # agar kiritilgan malumot isascii jadvalida
            # bol,asa lotin yozuviga aylantiriladi
        return super(AnnouncementCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('ann_detail', kwargs={'slug': self.object.slug})

#elonni uchirish
class AnnouncementDetailView(DetailView):
    model = Announcement
    context_object_name = 'object'
    template_name = 'announcement/ann_detail.html'
    success_message = "E'loningiz muvoffaqiyatli yaratildi! Bizning xizmatimizdan foydalanganingiz uchun raxmat!"

    def get_context_data(self, *args, **kwargs):
        obj = self.get_object()
        context = super().get_context_data()
        context['category'] = self.model.objects.filter(is_public=True, category=obj.category)[0:5]
        context['now'] = datetime.now()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context

    # def get_success_url(self, **kwargs):
    #     return reverse_lazy('ann_detail', kwargs={'slug': self.object.slug})


def edit_announcement(request, slug):
    announ = get_object_or_404(Announcement, slug=slug)
    form = AnnouncementForm(instance=announ)
    now = datetime.now()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announ)
        if form.is_valid():
            form.save()
            return render(request, 'announcement/add_and_update.html',
                          {'form': form, 'message': "E'loningiz muvoffaqiyatli o'zgartirildi!"})
    return render(request, 'announcement/add_and_update.html', {'form': form, 'now': now})


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
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'), is_public=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class SearchAnn(ListView):
    model = Announcement
    paginate_by = 3
    template_name = 'announcement/filter.html'
    # context_object_name = 'object_list'

    def get_queryset(self):
        query = self.request.GET.get('search')
        query_cat = self.request.GET.get('category')
        if query != '' and query is not None:
            object_list = self.model.objects.filter(
                (Q(translations__title__icontains=query) |
                 Q(translations__description__icontains=query)) &
                Q(is_public=True)
            )
        elif query_cat != '' and query_cat is not None:
            object_list = self.model.objects.filter(Q(category_id=query_cat) & Q(is_public=True))
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


# foydalanuvchilarni ro`yxatdan o`tkazish
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('announcement_list')
    template_name = 'accounts/sign_up.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class Login(LoginView):
    authentication_form = CustomAuthenticationForm
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        return context


class LogoutView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        auth_logout(self.request)
        return reverse('announcement_list')


def userprofile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            print()
            form.save()
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


class UserFilterListView(LoginRequiredMixin, ListView):
  model = Announcement
  template_name = "announcement/filter.html"
  context_object_name = 'object_list'
  paginate_by = 8

  def get_queryset(self):
      queryset = Announcement.objects.filter(created_by=self.request.user)
      return queryset
