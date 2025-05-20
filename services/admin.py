from django.contrib import admin
from .models import (
    Aminol_Official_Dealer,
    Aminol_Official_Dealer_Content,
    Aminol_Labaratory,
    Aminol_Logistics
)

class Aminol_Official_Dealer_ContentInline(admin.TabularInline):
    model = Aminol_Official_Dealer_Content
    extra = 1

@admin.register(Aminol_Official_Dealer)
class Aminol_Official_DealerAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_description')
    search_fields = ('title',)
    inlines = [Aminol_Official_Dealer_ContentInline]

@admin.register(Aminol_Official_Dealer_Content)
class Aminol_Official_Dealer_ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'aminol_official_dealer')
    search_fields = ('title',)
    list_filter = ('aminol_official_dealer',)

@admin.register(Aminol_Labaratory)
class Aminol_LabaratoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Aminol_Logistics)
class Aminol_LogisticsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)