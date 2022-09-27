from django.contrib import admin

from .models import User, Category, Genre, GenreTitle, Title, Comments, Review


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
            return 'Безимянный'
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
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comments)
