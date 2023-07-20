from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login

user_model = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:  # already linked
            return
        try:  # if user exists, connect the account to the existing account and login
            UserObj = user_model.objects.get(email=user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, UserObj, 'none')
        except user_model.DoesNotExist:
            pass
