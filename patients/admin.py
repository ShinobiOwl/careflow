from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'phone', 'gender', 'blood_group', 'is_active']
    list_filter = ['gender', 'blood_group', 'is_active']
    search_fields = ['first_name', 'last_name', 'patient_id', 'phone']
    readonly_fields = ['patient_id', 'registration_date']