from django.contrib import admin
from blog.models import Tag, Author, Article, Category
from Services.models import Announcement

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'id', 'author', 'publish_time', 'update_time', 'active')
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'startDate', 'endDate')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Announcement, AnnouncementAdmin)