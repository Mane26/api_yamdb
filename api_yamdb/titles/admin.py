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


class TitleInline(admin.TabularInline):
    model = Title.genre.through


class GenreAdmin(admin.ModelAdmin):
    """Страница произведений в админке."""
    list_display = ('pk', 'name', 'year', 'category')
    list_display_links = ('pk', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    model = Genre
    inlines = (
        TitleInline,
    )


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
