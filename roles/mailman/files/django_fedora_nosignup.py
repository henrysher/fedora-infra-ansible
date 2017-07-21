# Disable local signup

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoLocalSignUpAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False

class SignUpEnabledSocialAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True
