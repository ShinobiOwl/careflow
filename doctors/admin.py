from django.contrib import admin
from .models import Department, Doctor


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor_number', 'is_active']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_id', 'full_name', 'specialization', 'department', 'status', 'is_active']
    list_filter = ['department', 'gender', 'status', 'is_active']
    search_fields = ['first_name', 'last_name', 'specialization', 'doctor_id']
    readonly_fields = ['doctor_id']