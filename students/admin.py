from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'gender', 'phone']
    search_fields = ['name', 'email', 'phone']
