from django.contrib import admin

# Register your models here.

from social.models import Profile, Member, PrivateMessage, PublicMessage

admin.site.register(Profile)
admin.site.register(Member)
admin.site.register(PrivateMessage)
admin.site.register(PublicMessage)
