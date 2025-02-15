from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Thread, Board

def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Mark selected boards as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_inactive.short_description = "Mark selected boards as inactive"

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name', 'active')
    search_fields = ('name', 'long_name', 'description')
    list_filter = ('active',)
    ordering = ('name',)
    actions = [make_active, make_inactive]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('threads/', self.admin_site.admin_view(self.threads_view), name='threads_view'),
        ]
        return custom_urls + urls

    def threads_view(self, request):
        context = {}
        return render(request, 'admin/threads.html', context)

admin.site.register(Board, BoardAdmin)
admin.site.register(Thread)


