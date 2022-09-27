from django.contrib import admin

from .models import User, Category, Genre, GenreTitle, Title, Comments, Review

admin.site.empty_value_display = '-пусто-'


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
    )
    inlines = (GenreInline,)
    list_editable = ('category', )
    search_fields = ('name', )
    filter_horizontal = ('genre', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'pub_date',
        'text',
        'score',
    )
    list_editable = ('text', 'score')
    search_fields = ('author', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'pub_date',
        'text',
    )
    list_editable = ('text',)
    search_fields = ('author', 'review')


admin.site.register(User)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
