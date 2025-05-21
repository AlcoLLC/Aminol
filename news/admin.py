from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'

admin.site.register(News, NewsAdmin)