from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'pk',
        'username',
        'email',
        'bio',
        'role')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
