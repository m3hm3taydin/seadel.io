from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser

from django.contrib.sites.models import Site 
from django.contrib.auth.models import Group
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import Token
# from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

class CustomUserAdmin(UserAdmin):
    # add_form = 
    # form =
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)

# Hide some default admin sites

# admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(Token)
# admin.site.unregister(SocialAccount)
# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialToken)