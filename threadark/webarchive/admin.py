from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Thread
from .models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
    search_fields = ('name', 'description')
    list_filter = ('active',)
    ordering = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('/', self.admin_site.admin_view(self.threads_view), name='threads_view'),
        ]
        return custom_urls + urls

    def threads_view(self, request):
        context = {}
        return render(request, 'admin/threads.html', context)

admin.site.register(Board, BoardAdmin)
admin.site.register(Thread)


