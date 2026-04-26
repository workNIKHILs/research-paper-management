from django.contrib import admin
from .models import Faculty, Publication

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'joining_date']
    search_fields = ['name', 'department']
    list_filter = ['designation', 'department']

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'faculty', 'year', 'month']
    search_fields = ['title', 'faculty__name']
    list_filter = ['type', 'year', 'faculty__department']