from django.http import UnreadablePostError
from pylibmc import Error as MemcachedError

EXCLUDED = (
    UnreadablePostError,
    MemcachedError,
)

def exclude_useless_errors(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        for excluded_class in EXCLUDED:
            if isinstance(exc_value, excluded_class):
                return False
    return True


# Disable local signup

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoLocalSignUpAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False

class SignUpEnabledSocialAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return True
