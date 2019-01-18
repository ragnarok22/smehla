from django.contrib import admin

from news.models import News, Service


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_date')
    list_filter = ('pub_date',)


admin.site.register(News, NewsAdmin)
admin.site.register(Service)
