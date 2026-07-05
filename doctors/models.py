from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    floor_number = models.CharField(max_length=20, blank=True)
    phone_extension = models.CharField(max_length=10, blank=True)
    head_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('on_leave', 'On Leave'),
        ('on_duty', 'On Duty'),
        ('off_duty', 'Off Duty'),
        ('resigned', 'Resigned'),
    )

    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    medical_registration_number = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    available_days = models.CharField(max_length=200, default='Monday,Tuesday,Wednesday,Thursday,Friday')
    start_time = models.TimeField(default='09:00')
    end_time = models.TimeField(default='17:00')
    max_patients_per_day = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor_id} - Dr. {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            last_doctor = Doctor.objects.order_by('-id').first()
            last_id = last_doctor.id if last_doctor else 0
            self.doctor_id = f"DR{str(last_id + 1).zfill(6)}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"

    @property
    def short_name(self):
        return f"Dr. {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'