from django.contrib import admin

from .models import User, Category, Genre, GenreTitle, Title, Comments, Review


class GenreInline(admin.TabularInline):
    model = GenreTitle
    extra = 2


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'category',
        'year',
        'rating')
    inlines = (GenreInline,)
    list_editable = ('category', )
    search_fields = ('name', )
    list_filter = ('rating', )
    filter_horizontal = ('genre', )
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comments)
