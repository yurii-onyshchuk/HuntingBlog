from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from .models import User


class UserSingUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSingUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].help_text = ''

    class Meta:
        model = User
        fields = ('photo', 'username', 'first_name', 'last_name', 'email',)
