from django.contrib import admin
from .models import Faculty, Publication


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        'sl_no', 'faculty_name', 'title', 'type',
        'journal_conference', 'year', 'indexed', 'quartile'
    ]
    list_filter = ['indexed', 'year', 'type', 'quartile']
    search_fields = ['title', 'faculty_name', 'journal_conference']
    list_per_page = 25