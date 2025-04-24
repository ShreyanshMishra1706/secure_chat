from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

# admin.site.unregister(User)  # Unregister default registration
admin.site.register(User, UserAdmin)  # Re-register with UserAdmin
admin.site.register(CustomUser, UserAdmin)

