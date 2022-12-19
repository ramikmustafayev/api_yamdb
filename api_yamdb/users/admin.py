from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class UserAdmin(UserAdmin):
    list_display=('username','email','first_name','last_name','bio','role', 'is_staff','is_active')
   
    fieldsets = (
        (None, {'fields': ('username', 'email','first_name','last_name','bio','role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','password1', 'password2','first_name','last_name','bio','role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)