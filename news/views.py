from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from mysite import settings
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def send_mes(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['body'],
                             settings.EMAIL_HOST_USER,
                             list(form.cleaned_data['user']),
                             fail_silently=False,)
            if mail:
                messages.success(request, "Письмо успешно отправлено!")
                return redirect('send_mes')
            else:
                messages.error(request, "Ошибка при отправке")
    else:
        form = ContactForm()
    return render(request, 'send_mes.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect('home')
        else:
            messages.error(request, "Ошибка регистрации")

    else:
        form = UserRegisterForm()
    return render(request, 'sign_up.html', {"form": form})


def sign_in(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'sign_in.html', {"form": form})


def logout_user(request):
    logout(request)
    return redirect('sign_in')


class HomeNews(ListView):
    model = News
    template_name = 'home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# def index(request):
#     news = News.objects.all()
#     context = {'news': news, }
#     return render(request, 'scalper_index.html', context)

class NewsCategory(ListView):
    model = Category
    template_name = 'home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'category.html', {'news': news, 'category': category})


class ViewNews(DetailView):
    model = News
    template_name = 'view_news.html'
    context_object_name = 'news_item'


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'view_news.html', {'news_item': news_item})


class AddNews(CreateView):
    form_class = NewsForm
    template_name = 'add_news.html'

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         print(form)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'add_news.html', {'form': form})
