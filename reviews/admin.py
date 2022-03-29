from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'created', 'rank', 'text',)
    list_editable = ('text', 'rank',)
    list_filter = ('title', 'author',)
    search_fields = ('title', 'author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'review', 'author', 'text', 'created',)
    list_editable = ('text',)
    list_filter = ('created', 'author', 'title', 'review',)
    search_fields = ('author', 'title', 'review', 'text',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
