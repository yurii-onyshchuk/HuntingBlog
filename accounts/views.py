from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from . import forms
from .models import User


class UserRegister(CreateView):
    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/register.html'
    form_class = forms.UserRegisterForm

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return redirect('home')


class UserAuthentication(LoginView):
    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = forms.UserAuthenticationForm
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
    success_url = reverse_lazy('home')
    model = User

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class PersonalSafetyView(LoginRequiredMixin, TemplateView):
    extra_context = {'title': 'Безпека облікового запису',
                     'subtitle': 'Змінити пароль або видалити обліковий запис'}
    template_name = 'accounts/personal_cabinet/personal_safety.html'


class DeleteAccount(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'Видалення облікового запису'}
    success_url = reverse_lazy('login')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
