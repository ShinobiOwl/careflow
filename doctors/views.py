from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Department, Doctor
from .forms import DepartmentForm, DoctorForm


@login_required
def department_list(request):
    departments = Department.objects.filter(is_active=True)
    return render(request, 'doctors/department_list.html', {'departments': departments})


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'doctors/department_form.html', {'form': form, 'action': 'Create'})


@login_required
def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department {dept.name} updated!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'doctors/department_form.html', {'form': form, 'action': 'Update'})


@login_required
def doctor_list(request):
    doctors = Doctor.objects.filter(is_active=True)
    search = request.GET.get('search', '')
    if search:
        doctors = doctors.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(specialization__icontains=search) |
            Q(doctor_id__icontains=search)
        )
    dept = request.GET.get('department', '')
    if dept:
        doctors = doctors.filter(department_id=dept)
    status = request.GET.get('status', '')
    if status:
        doctors = doctors.filter(status=status)

    paginator = Paginator(doctors, 12)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page_obj': page_obj,
        'search': search,
        'departments': Department.objects.filter(is_active=True),
        'dept': dept,
        'status': status,
        'total': Doctor.objects.filter(is_active=True).count(),
    }
    return render(request, 'doctors/doctor_list.html', context)


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.select_related('patient').all()[:15]
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total_patients': doctor.appointments.values('patient').distinct().count(),
    }
    return render(request, 'doctors/doctor_detail.html', context)


@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'Doctor {doctor.full_name} added! ID: {doctor.doctor_id}')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'action': 'Add'})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Doctor {doctor.full_name} updated!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'action': 'Update', 'doctor': doctor})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_active = False
    doctor.status = 'resigned'
    doctor.save()
    messages.success(request, f'Doctor {doctor.full_name} deactivated.')
    return redirect('doctor_list')