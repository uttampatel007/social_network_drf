from django.contrib import admin
from .models import User, FriendRequest


admin.site.register(User)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'status']

admin.site.register(FriendRequest, FriendRequestAdmin)

