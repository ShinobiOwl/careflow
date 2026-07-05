from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm, AppointmentConsultForm


@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()

    search = request.GET.get('search', '')
    if search:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search) |
            Q(doctor__first_name__icontains=search) |
            Q(appointment_id__icontains=search) |
            Q(reason__icontains=search)
        )

    status = request.GET.get('status', '')
    if status:
        appointments = appointments.filter(status=status)

    date = request.GET.get('date', '')
    if date:
        appointments = appointments.filter(appointment_date=date)

    appt_type = request.GET.get('type', '')
    if appt_type:
        appointments = appointments.filter(appointment_type=appt_type)

    paginator = Paginator(appointments, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    today = timezone.now().date()
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'date': date,
        'appt_type': appt_type,
        'today_count': Appointment.objects.filter(appointment_date=today).count(),
        'pending_count': Appointment.objects.filter(status='scheduled').count(),
        'completed_count': Appointment.objects.filter(status='completed').count(),
    }
    return render(request, 'appointments/appointment_list.html', context)


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.save()
            messages.success(request, f'Appointment {appointment.appointment_id} booked!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(initial={'appointment_date': timezone.now().date()})
    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Book'})


@login_required
def appointment_consult(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentConsultForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Consultation updated for {appointment.appointment_id}!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentConsultForm(instance=appointment)
    return render(request, 'appointments/appointment_consult.html', {
        'form': form, 'appointment': appointment
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'cancelled'
    appointment.save()
    messages.warning(request, f'Appointment {appointment.appointment_id} cancelled.')
    return redirect('appointment_list')


@login_required
def appointment_status_update(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = status
    appointment.save()
    messages.success(request, f'Appointment marked as {appointment.get_status_display()}.')
    return redirect('appointment_detail', pk=appointment.pk)