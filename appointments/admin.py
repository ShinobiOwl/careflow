from django.contrib import admin
from .models import Appointment, Prescription, PrescriptionItem


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'priority']
    list_filter = ['status', 'appointment_type', 'priority', 'appointment_date']
    search_fields = ['appointment_id', 'patient__first_name', 'doctor__first_name']
    readonly_fields = ['appointment_id']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis', 'follow_up_days', 'created_at']


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine_name', 'dosage', 'frequency', 'duration']