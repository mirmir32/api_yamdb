from django.contrib import admin

from .models import Categories, Comment, Genre, Review, Title


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'categories')
    search_fields = ('name',)
    list_filter = ('year',)
    list_editable = ('categories',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'pub_date', 'score', 'text',)
    list_editable = ('text', 'score',)
    list_filter = ('title', 'author',)
    search_fields = ('title', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'review', 'author', 'text', 'pub_date',)
    list_editable = ('text',)
    list_filter = ('pub_date', 'author', 'title', 'review',)
    search_fields = ('author', 'title', 'review', 'text',)
    empty_value_display = '-пусто-'
