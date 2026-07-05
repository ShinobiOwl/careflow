import requests
import time
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import date

from .models import AIConversation, AIMessage
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

def get_careflow_context():
    """
    Gathers a summary of the current system state to provide context to the AI.
    """
    try:
        doctors = Doctor.objects.filter(is_active=True)
        total_doctors = doctors.count()
        available_doctors = doctors.filter(status="available").count()
        on_duty_doctors = doctors.filter(status="on_duty").count()
        on_leave_doctors = doctors.filter(status="on_leave").count()
        
        doctor_list = [f"{d.full_name} ({d.specialization}) - Status: {d.get_status_display()}" for d in doctors]
        
        patient_count = Patient.objects.filter(is_active=True).count()
        today_appts = Appointment.objects.filter(appointment_date=date.today()).count()
        
        context = "\n\n--- CURRENT CAREFLOW SYSTEM DATA ---\n"
        context += f"Total Active Patients: {patient_count}\n"
        context += f"Appointments Today: {today_appts}\n"
        context += "Doctor Staffing:\n"
        context += f"- Total Active Doctors: {total_doctors}\n"
        context += f"- Available Now: {available_doctors}\n"
        context += f"- On Duty: {on_duty_doctors}\n"
        context += f"- On Leave: {on_leave_doctors}\n"
        context += "Detailed Doctor List:\n"
        if doctor_list:
            context += "\n".join(doctor_list)
        else:
            context += "No active doctors found."
        context += "\n----------------------------------\n"
        return context
    except Exception as e:
        return f"\n(Error gathering system context: {str(e)})\n"
