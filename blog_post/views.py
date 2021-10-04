from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import Category, Blog, PicturesFromTheBlog, Tags, ContactMessage


def contact(request):
    return render(request, "Contact_us.html", {})


# Create your views here.
class HomePageView(ListView):
    template_name = 'index.html'
    queryset = Blog.objects.all()[:1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tags'] = Tags.objects.all()
        return context


class DetailViews(DetailView):
    model = Blog
    template_name = 'single.html'

    # def get_queryset(self):
    #     photos = Blog.objects.get(self.kwargs.get("slug"))
    #     return photos

    def get_context_data(self, **kwargs):
        context = super(DetailViews, self).get_context_data(**kwargs)
        return context


class BlogPageView(ListView):
    template_name = 'blog.html'
    queryset = Blog.objects.all()
    context_object_name = 'blogs'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['blogs'] = Blog.objects.all()
        return context


class CategoriesView(ListView):
    template_name = 'blog.html'
    model = Blog

    def get_queryset(self):
        queryset = self.model.objects.filter(category__slug=self.kwargs.get('slug'))
        return queryset


def tagsfilter(request, name):
    tags = get_object_or_404(Tags, name=name)
    all_tags = Tags.objects.all()
    nat = Blog.objects.filter(tags=tags)
    context = {
        "object_list": nat,
        "tags": all_tags
    }
    return render(request, "blog.html", context)


# contact qismidan xabar yuborish
def sendmail(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        msg = 'Sizga RISHTON24.uz saytidan ' + name + ' xabar yubordi. ' + '\n' + 'elektron pochtasi: ' + email + '\n' + 'xabar maqsadi: ' + subject + '\n' + 'xabar mazmuni: ' + '\n' + message
        send_mail(
            'Yangi xabar',
            msg,
            settings.EMAIL_HOST_USER,  # xabar jo`natuvchi elektron pochta
            ['sardorbek.uktamov.1@mail.ru'],  # xabar keluvchi elektron pochta
            fail_silently=False,
        )

        contact_user = ContactMessage(
            full_name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_user.save()
        messages.info(request, "Xabaringiz muvoffaqiyatli yuborildi! Tez orada elektron pochtangizga javobini olasiz.")
        return redirect('contact')
