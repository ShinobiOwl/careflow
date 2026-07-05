from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):
    patients = Patient.objects.filter(is_active=True)

    search = request.GET.get('search', '')
    if search:
        patients = patients.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(patient_id__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    gender = request.GET.get('gender', '')
    if gender:
        patients = patients.filter(gender=gender)

    blood = request.GET.get('blood_group', '')
    if blood:
        patients = patients.filter(blood_group=blood)

    sort = request.GET.get('sort', '-created_at')
    patients = patients.order_by(sort)

    paginator = Paginator(patients, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page_obj': page_obj,
        'search': search,
        'gender': gender,
        'blood': blood,
        'sort': sort,
        'total': Patient.objects.filter(is_active=True).count(),
    }
    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related('doctor').all()
    context = {
        'patient': patient,
        'appointments': appointments,
        'appointment_count': appointments.count(),
        'completed_count': appointments.filter(status='completed').count(),
    }
    return render(request, 'patients/patient_detail.html', context)


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} registered! ID: {patient.patient_id}')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form, 'action': 'Register'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.full_name} updated!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'action': 'Update', 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.is_active = False
    patient.save()
    messages.success(request, f'Patient {patient.full_name} deactivated.')
    return redirect('patient_list')