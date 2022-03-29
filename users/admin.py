from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'bio',
        'role')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
