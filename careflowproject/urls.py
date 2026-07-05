"""
URL configuration for careflowproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    from patients.models import Patient
    from doctors.models import Doctor, Department
    from appointments.models import Appointment

    today = timezone.now().date()

    context = {
        'total_patients': Patient.objects.filter(is_active=True).count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'total_departments': Department.objects.filter(is_active=True).count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'scheduled_count': Appointment.objects.filter(status='scheduled').count(),
        'completed_count': Appointment.objects.filter(status='completed').count(),
        'in_consultation': Appointment.objects.filter(status='in_consultation').count(),
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:8],
        'today_appointment_list': Appointment.objects.select_related('patient', 'doctor').filter(appointment_date=today).order_by('appointment_time'),
        'recent_patients': Patient.objects.filter(is_active=True).order_by('-created_at')[:5],
        'available_doctors': Doctor.objects.filter(is_active=True, status='available'),
    }
    from django.shortcuts import render
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('ai/', include('ai_assistant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
