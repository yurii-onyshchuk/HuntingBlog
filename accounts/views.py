from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from . import forms
from .models import User
from .utils import RedirectAuthenticatedUserMixin


class UserSignUp(RedirectAuthenticatedUserMixin, CreateView):
    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/signup.html'
    form_class = forms.UserSingUpForm
    redirect_authenticated_user_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return redirect('home')


class UserAuthentication(LoginView):
    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


class PersonalCabinet(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Особистий кабінет',
                     'subtitle': 'Керуйте своїми особистими даними та безпекою акаунту'}
    template_name = 'accounts/personal_cabinet/personal_cabinet.html'


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Особисті дані',
                     'subtitle': 'Керуйте своїми особистими та контактними даними'}
    template_name = 'accounts/personal_cabinet/personal_info.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('personal_cabinet')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


@login_required
def user_avatar_change(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        user.photo = request.FILES['user_photo']
        user.save_thumbnail()
    return redirect('personal_info', slug=request.user.slug)


@login_required
def user_avatar_delete(request):
    if request.method == 'POST':
        User.objects.get(pk=request.user.pk).photo.delete(save=True)
    return redirect('personal_info', slug=request.user.slug)


class PersonalSafetyView(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Безпека облікового запису',
                     'subtitle': 'Змінити пароль або видалити обліковий запис'}
    template_name = 'accounts/personal_cabinet/personal_safety.html'


class DeleteAccount(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'Видалення облікового запису'}
    success_url = reverse_lazy('login')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
