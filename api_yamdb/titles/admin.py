from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    """Страница категорий в админке."""
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class GenreAdmin(admin.ModelAdmin):
    """Страница жанров в админке."""
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    """Страница произведений в админке."""
    list_display = ('pk', 'name', 'year', 'category')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
