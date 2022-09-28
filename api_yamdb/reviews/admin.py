from django.contrib import admin

from .models import User, Category, Genre, GenreTitle, Title, Comments, Review

admin.site.empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'full_name',
        'role',
    )
    list_editable = ('role',)
    search_fields = ('email', 'username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'

    def full_name(self, obj,):
        if not obj.get_full_name():
            return 'Безымянный'
        return obj.get_full_name()

    full_name.short_description = 'Полное имя'


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


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentAdmin)
