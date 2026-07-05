
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careflowproject.settings')
django.setup()

from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone
from ai_assistant.views import get_db_context

def test_context():
    query = "available doctors?"
    print(f"Testing query: {query}")
    context = get_db_context(query)
    print("\n--- GENERATED CONTEXT ---")
    print(context)
    print("--- END CONTEXT ---\n")

    # Also check the database directly
    print("Database Check:")
    print(f"Total Active Doctors: {Doctor.objects.filter(is_active=True).count()}")
    print(f"Available Doctors: {Doctor.objects.filter(is_active=True, status='available').count()}")
    
    doctors = Doctor.objects.filter(is_active=True)
    for d in doctors:
        print(f"{d.full_name} - {d.status}")

if __name__ == "__main__":
    test_context()
