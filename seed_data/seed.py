"""
CareFlow Realistic Hospital Data Seeder
Run: python manage.py shell < seed_data/seed.py
  or: python manage.py shell
      >>> exec(open('seed_data/seed.py').read())
"""

from datetime import date, time, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from patients.models import Patient
from doctors.models import Department, Doctor
from appointments.models import Appointment
import random

print("🏥 Seeding CareFlow Database...")

# ─── Create Superuser ───
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@careflow.hospital',
        password='Admin@2025',
        first_name='Super',
        last_name='Admin'
    )
    Profile.objects.create(
        user=admin_user,
        role='admin',
        phone='9876543210',
        gender='Male',
        date_of_birth=date(1985, 6, 15),
    )
    print("✅ Superuser created: admin / Admin@2025")

# ─── Create Staff Users ───
staff_data = [
    ('receptionist1', 'Priya', 'Sharma', 'receptionist', '9876543211', 'Female', date(1992, 3, 22)),
    ('receptionist2', 'Kavitha', 'Rajendran', 'receptionist', '9876543212', 'Female', date(1995, 7, 10)),
    ('nurse1', 'Anitha', 'Kumar', 'nurse', '9876543213', 'Female', date(1990, 11, 5)),
    ('nurse2', 'Meena', 'Devi', 'nurse', '9876543214', 'Female', date(1988, 1, 18)),
    ('pharmacist1', 'Ravi', 'Chandran', 'pharmacist', '9876543215', 'Male', date(1987, 9, 30)),
    ('labtech1', 'Suresh', 'Babu', 'lab_tech', '9876543216', 'Male', date(1993, 4, 14)),
]

for username, fn, ln, role, phone, gender, dob in staff_data:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f'{username}@careflow.hospital',
            password='Staff@2024',
            first_name=fn,
            last_name=ln,
        )
        Profile.objects.create(user=user, role=role, phone=phone, gender=gender, date_of_birth=dob)
        print(f"✅ Staff: {fn} {ln} ({role})")

# ─── Create Departments ───
departments_data = [
    ('General Medicine', 'Primary care and general health consultations', '1st Floor', '101'),
    ('Cardiology', 'Heart and cardiovascular system care', '2nd Floor', '201'),
    ('Orthopedics', 'Bone, joint, and musculoskeletal care', '2nd Floor', '202'),
    ('Pediatrics', 'Medical care for infants and children', '1st Floor', '102'),
    ('Neurology', 'Brain and nervous system disorders', '3rd Floor', '301'),
    ('Dermatology', 'Skin, hair, and nail conditions', '3rd Floor', '302'),
    ('ENT', 'Ear, Nose, and Throat specialist', '1st Floor', '103'),
    ('Ophthalmology', 'Eye care and vision treatment', '3rd Floor', '303'),
    ('Gynecology', 'Women health and pregnancy care', '2nd Floor', '203'),
    ('Pulmonology', 'Respiratory and lung care', '4th Floor', '401'),
    ('Gastroenterology', 'Digestive system disorders', '4th Floor', '402'),
    ('Psychiatry', 'Mental health and behavioral disorders', '4th Floor', '403'),
    ('Urology', 'Urinary tract and male reproductive health', '4th Floor', '404'),
    ('Oncology', 'Cancer diagnosis and treatment', '5th Floor', '501'),
    ('Radiology', 'Medical imaging and diagnostics', 'Ground Floor', 'G01'),
]

departments = {}
for name, desc, floor, ext in departments_data:
    dept, created = Department.objects.get_or_create(
        name=name,
        defaults={'description': desc, 'floor_number': floor, 'phone_extension': ext}
    )
    departments[name] = dept
    if created:
        print(f"✅ Department: {name}")

# ─── Create Doctors (Realistic Indian Names) ───
doctors_data = [
    ('Rajesh', 'Krishnamurthy', 'M', 'General Medicine', 'Internal Medicine', 'MBBS, MD (General Medicine)', 'TMC-2010-4521', 18, 800, '9445011001'),
    ('Lakshmi', 'Venkataraman', 'F', 'Cardiology', 'Interventional Cardiology', 'MBBS, MD, DM (Cardiology)', 'TMC-2008-3321', 22, 1500, '9445011002'),
    ('Senthil', 'Nathan', 'M', 'Orthopedics', 'Joint Replacement Surgery', 'MBBS, MS (Ortho)', 'TMC-2012-5678', 14, 1200, '9445011003'),
    ('Deepa', 'Subramaniam', 'F', 'Pediatrics', 'Neonatology', 'MBBS, MD (Pediatrics), Fellowship', 'TMC-2014-7890', 10, 700, '9445011004'),
    ('Venkatesh', 'Iyer', 'M', 'Neurology', 'Stroke & Epilepsy', 'MBBS, MD, DM (Neurology)', 'TMC-2009-2345', 20, 1400, '9445011005'),
    ('Nirmala', 'Devarajan', 'F', 'Dermatology', 'Cosmetic Dermatology', 'MBBS, MD (Dermatology)', 'TMC-2015-6789', 9, 900, '9445011006'),
    ('Karthik', 'Pillai', 'M', 'ENT', 'Head & Neck Surgery', 'MBBS, MS (ENT)', 'TMC-2013-4567', 12, 800, '9445011007'),
    ('Sangeetha', 'Raman', 'F', 'Ophthalmology', 'Retina Specialist', 'MBBS, MS (Ophthal)', 'TMC-2016-1234', 8, 1000, '9445011008'),
    ('Prabhu', 'Gopalakrishnan', 'M', 'Gynecology', 'Obstetrics & Gynecology', 'MBBS, MS (OBG)', 'TMC-2011-9012', 16, 900, '9445011009'),
    ('Revathi', 'Menon', 'F', 'Pulmonology', 'Pulmonary Medicine', 'MBBS, MD (Pulmonology)', 'TMC-2017-3456', 7, 850, '9445011010'),
    ('Arunachalam', 'Swaminathan', 'M', 'Gastroenterology', 'Hepatology', 'MBBS, MD, DM (Gastro)', 'TMC-2007-7891', 24, 1300, '9445011011'),
    ('Bharathi', 'Raghunathan', 'F', 'Psychiatry', 'Clinical Psychology', 'MBBS, MD (Psychiatry)', 'TMC-2018-2341', 6, 750, '9445011012'),
    ('Muthu', 'Kumarasamy', 'M', 'Urology', 'Uro-oncology', 'MBBS, MS, MCh (Urology)', 'TMC-2010-5672', 17, 1400, '9445011013'),
    ('Vasanthi', 'Parameswaran', 'F', 'Oncology', 'Medical Oncology', 'MBBS, MD, DM (Oncology)', 'TMC-2012-8903', 15, 1600, '9445011014'),
    ('Ganesh', 'Balasubramanian', 'M', 'Radiology', 'Diagnostic Radiology', 'MBBS, MD (Radiology)', 'TMC-2014-1235', 11, 600, '9445011015'),
    ('Uma', 'Shankar', 'F', 'General Medicine', 'Family Medicine', 'MBBS, DNB (Family Medicine)', 'TMC-2019-4568', 5, 500, '9445011016'),
    ('Thiagarajan', 'Ramanathan', 'M', 'Cardiology', 'Electrophysiology', 'MBBS, MD, DM (Cardiology)', 'TMC-2006-7894', 26, 1800, '9445011017'),
    ('Padma', 'Priya', 'F', 'Pediatrics', 'Pediatric Neurology', 'MBBS, MD (Pediatrics)', 'TMC-2016-0123', 8, 750, '9445011018'),
    ('Saravanan', 'Muthusamy', 'M', 'Orthopedics', 'Spine Surgery', 'MBBS, MS, Fellowship', 'TMC-2011-3452', 16, 1350, '9445011019'),
    ('Jayanthi', 'Krishnan', 'F', 'Dermatology', 'Pediatric Dermatology', 'MBBS, MD (Dermatology)', 'TMC-2020-6785', 4, 650, '9445011020'),
]

doctors = []
for fn, ln, g, dept_name, spec, qual, reg, exp, fee, phone in doctors_data:
    dob_year = 2024 - exp - 27
    doctor, created = Doctor.objects.get_or_create(
        medical_registration_number=reg,
        defaults={
            'first_name': fn,
            'last_name': ln,
            'email': f'dr.{fn.lower()}.{ln.lower()}@careflow.hospital',
            'phone': phone,
            'date_of_birth': date(dob_year, random.randint(1, 12), random.randint(1, 28)),
            'gender': g,
            'department': departments[dept_name],
            'specialization': spec,
            'qualification': qual,
            'experience_years': exp,
            'consultation_fee': fee,
            'status': random.choice(['available', 'available', 'available', 'on_duty']),
            'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday',
            'start_time': time(9, 0),
            'end_time': time(17, 0),
            'max_patients_per_day': random.choice([15, 20, 25]),
            'bio': f'Senior consultant with {exp} years of experience in {spec}.',
        }
    )
    doctors.append(doctor)
    if created:
        print(f"✅ Doctor: Dr. {fn} {ln} ({spec})")

# Set department heads
for dept_name in departments:
    dept_doctor = Doctor.objects.filter(department=departments[dept_name]).first()
    if dept_doctor:
        departments[dept_name].head_doctor = dept_doctor
        departments[dept_name].save()

# ─── Create Patients (Realistic Indian People) ───
patients_data = [
    # (first_name, last_name, gender, dob, phone, email, blood_group, marital, address, city, state, pincode, emergency_name, emergency_phone, emergency_relation, medical_history, chronic, allergies, medications, insurance_provider, insurance_policy)
    ('Arul', 'Murugan', 'Male', date(1975, 5, 12), '9786543201', 'arul.murugan@gmail.com', 'B+', 'Married', '14, Temple Street, Anna Nagar', 'Thoothukudi', 'Tamil Nadu', '628001', 'Meena Murugan', '9786543202', 'Wife', 'Hypertension diagnosed 2018', 'Hypertension', 'None', 'Amlodipine 5mg', 'Star Health', 'SH-2021-45678'),
    ('Bhanumathi', 'Radhakrishnan', 'Female', date(1982, 8, 25), '9786543203', 'bhanumathi.r@gmail.com', 'O+', 'Married', '23, Nehruji Road, K.K. Nagar', 'Madurai', 'Tamil Nadu', '625020', 'Radhakrishnan S', '9786543204', 'Husband', 'Gestational diabetes during pregnancy 2019', 'Diabetes Type 2', 'Penicillin', 'Metformin 500mg', 'New India Assurance', 'NIA-2020-12345'),
    ('Chandru', 'Balakrishnan', 'Male', date(1990, 2, 14), '9786543205', 'chandru.bala@outlook.com', 'A-', 'Single', '7/3, Cross Road, Besant Nagar', 'Chennai', 'Tamil Nadu', '600090', 'Balakrishnan V', '9786543206', 'Father', 'ACL tear surgery 2021', 'None', 'None', 'None', 'HDFC ERGO', 'HE-2022-67890'),
    ('Devika', 'Ramaswamy', 'Female', date(1995, 11, 3), '9786543207', 'devika.ramaswamy@yahoo.com', 'AB+', 'Single', '45, Poes Garden, T. Nagar', 'Chennai', 'Tamil Nadu', '600017', 'Ramaswamy K', '9786543208', 'Father', 'None', 'None', 'Dust allergy', 'Cetirizine PRN', 'ICICI Lombard', 'IL-2023-11111'),
    ('Ezhil', 'Arasu', 'Male', date(1968, 7, 20), '9786543209', 'ezhil.arasu@gmail.com', 'B-', 'Married', '12, Raja Street, Salem Fort', 'Salem', 'Tamil Nadu', '636001', 'Lakshmi Arasu', '9786543210', 'Wife', 'Type 2 Diabetes, Diabetic retinopathy 2020', 'Diabetes Type 2', 'Sulfa drugs', 'Insulin, Metformin', 'Star Health', 'SH-2019-22222'),
    ('Farida', 'Begum', 'Female', date(1988, 3, 8), '9786543211', 'farida.begum@gmail.com', 'O-', 'Married', '8, Mosque Street, Triplicane', 'Chennai', 'Tamil Nadu', '600005', 'Abdul Rahman', '9786543212', 'Husband', 'PCOS diagnosed 2016', 'PCOS', 'None', 'OCP', 'United India Insurance', 'UI-2021-33333'),
    ('Ganesh', 'Moorthy', 'Male', date(1955, 12, 1), '9786543213', 'ganesh.moorthy@gmail.com', 'A+', 'Widowed', '3, Agraharam Street, Srirangam', 'Tiruchirappalli', 'Tamil Nadu', '620006', 'Moorthy S', '9786543214', 'Son', 'CABG 2019, Chronic kidney disease Stage 3', 'CKD, CAD', 'Aspirin allergy', 'Atorvastatin, Clopidogrel', 'New India Assurance', 'NIA-2018-44444'),
    ('Hari', 'Prasad', 'Male', date(1998, 6, 17), '9786543215', 'hari.prasad@outlook.com', 'O+', 'Single', '56, IT Corridor, Sholinganallur', 'Chennai', 'Tamil Nadu', '600119', 'Venkat Prasad', '9786543216', 'Father', 'None', 'None', 'None', 'None', 'Star Health', 'SH-2023-55555'),
    ('Indira', 'Gandhi', 'Female', date(1972, 9, 30), '9786543217', 'indira.g1972@gmail.com', 'B+', 'Divorced', '19, Mount Road, Guindy', 'Chennai', 'Tamil Nadu', '600032', 'Kavitha', '9786543218', 'Sister', 'Breast cancer survivor 2020, Hypothyroidism', 'Hypothyroidism', 'Codeine', 'Levothyroxine', 'HDFC ERGO', 'HE-2020-66666'),
    ('Jagan', 'Mohan', 'Male', date(1985, 4, 22), '9786543219', 'jagan.mohan@gmail.com', 'AB-', 'Married', '78, Park Street, Nungambakkam', 'Chennai', 'Tamil Nadu', '600034', 'Priya Mohan', '9786543220', 'Wife', 'Asthma since childhood', 'Bronchial Asthma', 'Aspirin', 'Montelukast, Formoterol', 'ICICI Lombard', 'IL-2022-77777'),
    ('Kamala', 'Subramanian', 'Female', date(2000, 1, 15), '9786543221', 'kamala.sub@gmail.com', 'A+', 'Single', '33, Bazaar Street, Mylapore', 'Chennai', 'Tamil Nadu', '600004', 'Subramanian R', '9786543222', 'Father', 'None', 'None', 'Latex', 'None', 'Star Health', 'SH-2023-88888'),
    ('Lakshmanan', 'Iyer', 'Male', date(1948, 10, 8), '9786543223', 'lakshmanan.iyer@gmail.com', 'O+', 'Married', '5, Brahmin Street, Kumbakonam', 'Kumbakonam', 'Tamil Nadu', '612001', 'Janaki Iyer', '9786543224', 'Wife', 'Parkinsons disease 2017, Benign prostatic hyperplasia', 'Parkinsons, BPH', 'None', 'Levodopa, Tamsulosin', 'United India Insurance', 'UI-2017-99999'),
    ('Mahalakshmi', 'Venkatesh', 'Female', date(1993, 5, 28), '9786543225', 'maha.venkatesh@gmail.com', 'B+', 'Married', '22, Lake View Road, Erode', 'Erode', 'Tamil Nadu', '638001', 'Venkatesh R', '9786543226', 'Husband', 'Anxiety disorder, Migraine', 'Migraine', 'None', 'Sumatriptan, Escitalopram', 'New India Assurance', 'NIA-2022-10101'),
    ('Natarajan', 'Pillai', 'Male', date(1962, 3, 11), '9786543227', 'nat.pillai@gmail.com', 'A-', 'Married', '8, Palace Road, Padmanabhapuram', 'Nagercoil', 'Tamil Nadu', '629001', 'Saroja Pillai', '9786543228', 'Wife', 'COPD, Former smoker (quit 2015)', 'COPD', 'None', 'Tiotropium, Salbutamol', 'Star Health', 'SH-2018-20202'),
    ('Oviya', 'Saravanan', 'Female', date(2001, 8, 19), '9786543229', 'oviya.saravanan@gmail.com', 'O+', 'Single', '14, Beach Road, Palavakkam', 'Chennai', 'Tamil Nadu', '600041', 'Saravanan M', '9786543230', 'Father', 'Epilepsy since age 12', 'Epilepsy', 'None', 'Valproate', 'HDFC ERGO', 'HE-2023-30303'),
    ('Prakash', 'Rao', 'Male', date(1978, 12, 5), '9786543231', 'prakash.rao@gmail.com', 'B-', 'Married', '67, Gandhi Road, Vellore', 'Vellore', 'Tamil Nadu', '632001', 'Anitha Rao', '9786543232', 'Wife', 'Rheumatoid arthritis 2019', 'Rheumatoid Arthritis', 'NSAIDs', 'Methotrexate, Folic acid', 'ICICI Lombard', 'IL-2021-40404'),
    ('Rajalakshmi', 'Narayanan', 'Female', date(1958, 6, 30), '9786543233', 'raji.narayanan@gmail.com', 'AB+', 'Widowed', '3, Kalakshetra Road, Adyar', 'Chennai', 'Tamil Nadu', '600020', 'Srinivasan N', '9786543234', 'Son', 'Osteoporosis, Cataract surgery 2022', 'Osteoporosis', 'Penicillin', 'Alendronate, Calcium', 'United India Insurance', 'UI-2019-50505'),
    ('Sivakumar', 'Naidu', 'Male', date(1983, 2, 9), '9786543235', 'siva.naidu@gmail.com', 'O-', 'Married', '91, Ring Road, Coimbatore', 'Coimbatore', 'Tamil Nadu', '641001', 'Latha Naidu', '9786543236', 'Wife', 'Gallbladder removal 2020', 'None', 'Morphine', 'None', 'Star Health', 'SH-2020-60606'),
    ('Thangam', 'Joseph', 'Female', date(1997, 4, 14), '9786543237', 'thangam.joseph@gmail.com', 'A+', 'Single', '28, Church Street, Vallioor', 'Tirunelveli', 'Tamil Nadu', '627117', 'Joseph A', '9786543238', 'Father', 'Anemia, Iron deficiency', 'Iron deficiency anemia', 'None', 'Iron supplements', 'New India Assurance', 'NIA-2023-70707'),
    ('Udhaya', 'Kumar', 'Male', date(1970, 7, 7), '9786543239', 'udhaya.kumar@gmail.com', 'B+', 'Married', '42, Main Road, Sivanthakulam', 'Thoothukudi', 'Tamil Nadu', '628002', 'Selvi Kumar', '9786543240', 'Wife', 'Hepatitis B carrier, Liver cirrhosis Stage 2', 'Hepatitis B, Liver Cirrhosis', 'None', 'Entecavir', 'HDFC ERGO', 'HE-2019-80808'),
    ('Vanitha', 'Mani', 'Female', date(1991, 9, 23), '9786543241', 'vanitha.mani@gmail.com', 'O+', 'Married', '15, Garden Street, Pollachi', 'Pollachi', 'Tamil Nadu', '642001', 'Mani K', '9786543242', 'Husband', 'Gestational diabetes 2022, Urinary tract infection recurrent', 'None currently', 'Sulfonamides', 'None currently', 'ICICI Lombard', 'IL-2022-90909'),
    ('Yogesh', 'Babu', 'Male', date(2003, 3, 16), '9786543243', 'yogesh.babu@gmail.com', 'AB-', 'Single', '6, Railway Colony, Tiruppur', 'Tiruppur', 'Tamil Nadu', '641601', 'Babu R', '9786543244', 'Father', 'ACL injury football 2023', 'None', 'None', 'None', 'Star Health', 'SH-2023-01010'),
    ('Zeenath', 'Beevi', 'Female', date(1965, 11, 12), '9786543245', 'zeenath.beevi@gmail.com', 'A+', 'Married', '9, Kaja Nagar, Tirunelveli Town', 'Tirunelveli', 'Tamil Nadu', '627001', 'Abdul Kadar', '9786543246', 'Husband', 'Type 2 Diabetes, Diabetic neuropathy, Hypertension', 'Diabetes Type 2, Hypertension', 'None', 'Glimepiride, Telmisartan', 'United India Insurance', 'UI-2018-11110'),
    ('Akash', 'Selvan', 'Male', date(1996, 1, 28), '9786543247', 'akash.selvan@gmail.com', 'B+', 'Single', '1, Sivanthakulam 1st Street', 'Thoothukudi', 'Tamil Nadu', '628003', 'Selvan K', '9786543248', 'Father', 'Appendectomy 2019', 'None', 'Latex', 'None', 'HDFC ERGO', 'HE-2022-21212'),
    ('Bharath', 'Srinivasan', 'Male', date(1987, 10, 3), '9786543249', 'bharath.srini@gmail.com', 'O+', 'Married', '55, OMR Road, Perungudi', 'Chennai', 'Tamil Nadu', '600096', 'Divya Srinivasan', '9786543250', 'Wife', 'Lumbar disc herniation L4-L5 2021', 'None', 'None', 'Pregabalin PRN', 'ICICI Lombard', 'IL-2021-31313'),
    ('Chitra', 'Devi', 'Female', date(1974, 8, 16), '9786543251', 'chitra.devi@gmail.com', 'B-', 'Married', '31, VOC Street, Virudhunagar', 'Virudhunagar', 'Tamil Nadu', '626001', 'Devi Raj', '9786543252', 'Husband', 'Breast lump (benign fibroadenoma), Thyroid nodule', 'Hypothyroidism', 'Iodine contrast', 'Levothyroxine', 'Star Health', 'SH-2022-41414'),
    ('Dinesh', 'Karthik', 'Male', date(1999, 5, 20), '9786543253', 'dinesh.karthik@gmail.com', 'AB+', 'Single', '12, Techno Park, Taramani', 'Chennai', 'Tamil Nadu', '600113', 'Karthik R', '9786543254', 'Father', 'Recurrent tonsillitis', 'None', 'Amoxicillin', 'None', 'New India Assurance', 'NIA-2023-51515'),
    ('Eswari', 'Pandian', 'Female', date(1952, 2, 28), '9786543255', 'eswari.pandian@gmail.com', 'O-', 'Widowed', '8, West Car Street, Karaikudi', 'Karaikudi', 'Tamil Nadu', '630001', 'Pandian M', '9786543256', 'Son', 'Osteoarthritis both knees, Hearing loss', 'Osteoarthritis', 'NSAIDs', 'Paracetamol, Diclofenac gel', 'United India Insurance', 'UI-2016-61616'),
    ('Franklin', 'Raj', 'Male', date(1976, 6, 9), '9786543257', 'franklin.raj@gmail.com', 'A+', 'Married', '44, Pudur Main Road, Madurai', 'Madurai', 'Tamil Nadu', '625016', 'Diana Raj', '9786543258', 'Wife', 'Kidney stones (recurrent), Hyperuricemia', 'Gout', 'Allopurinol allergy', 'Febuxostat', 'HDFC ERGO', 'HE-2020-71717'),
    ('Gayathri', 'Ravi', 'Female', date(2002, 12, 25), '9786543259', 'gayathri.ravi@gmail.com', 'O+', 'Single', '17, College Road, Thanjavur', 'Thanjavur', 'Tamil Nadu', '613001', 'Ravi Shankar', '9786543260', 'Father', 'PCOS, Obesity', 'PCOS, Obesity', 'None', 'Metformin', 'Star Health', 'SH-2023-81818'),
]

patients = []
for data in patients_data:
    fn, ln, g, dob, phone, email, bg, ms, addr, city, state, pin, em_name, em_phone, em_rel, mh, cc, al, med, ins, pol = data
    patient, created = Patient.objects.get_or_create(
        phone=phone,
        defaults={
            'first_name': fn, 'last_name': ln, 'email': email,
            'date_of_birth': dob, 'gender': g, 'blood_group': bg,
            'marital_status': ms, 'address': addr, 'city': city,
            'state': state, 'pincode': pin,
            'emergency_contact_name': em_name, 'emergency_contact_phone': em_phone,
            'emergency_contact_relation': em_rel,
            'medical_history': mh, 'chronic_conditions': cc,
            'allergies': al, 'current_medications': med,
            'insurance_provider': ins, 'insurance_policy_number': pol,
        }
    )
    patients.append(patient)
    if created:
        print(f"✅ Patient: {fn} {ln} ({bg}, {g})")

# ─── Create Appointments ───
today = date.today()
statuses = ['scheduled', 'confirmed', 'checked_in', 'completed', 'completed', 'completed', 'cancelled', 'no_show']
types = ['consultation', 'follow_up', 'routine_checkup', 'emergency', 'lab_review', 'vaccination', 'surgery_consult']
priorities = ['normal', 'normal', 'normal', 'normal', 'urgent', 'emergency']
reasons = [
    'Persistent headache for 2 weeks', 'Routine blood pressure check',
    'Chest pain and shortness of breath', 'Follow-up for diabetes management',
    'Knee pain while walking', 'Childhood vaccination schedule',
    'Skin rash on arms and legs', 'Follow-up after surgery',
    'Recurring stomach pain', 'Vision problems and eye strain',
    'Pregnancy checkup - 3rd trimester', 'Cough and fever for 5 days',
    'Anxiety and sleep disturbances', 'Blood in urine',
    'Post-chemotherapy follow-up', 'Annual health checkup',
    'Severe lower back pain', 'Allergic reaction - hives',
    'Thyroid medication review', 'Shoulder pain and stiffness',
]
symptoms_list = [
    'Headache, dizziness, nausea', 'BP reading elevated',
    'Chest tightness, sweating, palpitation', 'Fasting sugar: 180mg/dL',
    'Swelling in right knee, pain climbing stairs', 'No symptoms - vaccination visit',
    'Red itchy patches on forearms', 'Post-op wound healing well',
    'Abdominal pain after meals, bloating', 'Blurred vision, eye fatigue',
    'Swelling in feet, baby movement normal', 'Dry cough, fever 101°F, body ache',
    'Insomnia, racing thoughts, tremors', 'Hematuria, flank pain',
    'Fatigue, nausea, low WBC count', 'No complaints - preventive visit',
    'Pain radiating to left leg, numbness', 'Widespread hives, itching, mild swelling',
    'TSH elevated at 8.5', 'Limited range of motion, pain at night',
]
vital_signs_list = [
    'BP: 150/95, Pulse: 82, Temp: 98.4°F, SpO2: 98%',
    'BP: 140/90, Pulse: 76, Temp: 98.6°F, SpO2: 99%',
    'BP: 110/70, Pulse: 96, Temp: 98.8°F, SpO2: 96%',
    '',  # no vitals for some
    'BP: 130/85, Pulse: 74, Temp: 98.6°F, SpO2: 99%',
]
diagnoses = [
    'Tension headache - stress related', 'Essential hypertension - well controlled',
    'Acute coronary syndrome - unstable angina', 'Type 2 Diabetes - uncontrolled',
    'Osteoarthritis right knee - Grade 3', 'Vaccination administered',
    'Contact dermatitis - likely allergic reaction', 'Post-operative recovery - satisfactory',
    'Gastritis - H.pylori suspected', 'Refractive error - myopia',
    'Pregnancy - 32 weeks, normal', 'Upper respiratory tract infection',
    'Generalized anxiety disorder', 'Urolithiasis - left kidney stone 6mm',
    'Post-chemotherapy - partial remission', 'Healthy - all parameters normal',
    'Lumbar radiculopathy L5-S1', 'Acute urticaria - allergen exposure',
    'Hypothyroidism - medication adjustment needed', 'Frozen shoulder - adhesive capsulitis',
]

appointment_count = 0
for i in range(50):
    day_offset = random.randint(-30, 15)
    appt_date = today + timedelta(days=day_offset)

    if appt_date <= today:
        status = random.choice(['completed', 'completed', 'completed', 'cancelled', 'no_show', 'in_consultation'])
    else:
        status = random.choice(['scheduled', 'confirmed', 'scheduled'])

    hour = random.randint(9, 16)
    minute = random.choice([0, 15, 30, 45])

    patient = random.choice(patients)
    doctor = random.choice(doctors)

    appt = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        appointment_date=appt_date,
        appointment_time=time(hour, minute),
        appointment_type=random.choice(types),
        status=status,
        priority=random.choice(priorities),
        reason=random.choice(reasons),
        symptoms=random.choice(symptoms_list),
    )

    if status == 'completed':
        appt.vital_signs = random.choice(vital_signs_list)
        appt.diagnosis = random.choice(diagnoses)
        appt.prescription = 'Tab. Paracetamol 500mg TID x 5 days\nTab. Omeprazole 20mg OD before breakfast x 2 weeks'
        appt.notes = 'Patient advised to follow up in 2 weeks. Continue current medications.'
        appt.follow_up_date = appt_date + timedelta(days=random.choice([7, 14, 21, 30]))
        appt.save()

    appointment_count += 1

print(f"✅ Created {appointment_count} appointments")

print("\n" + "="*50)
print("🏥 CareFlow Database Seeding Complete!")
print("="*50)
print(f"  Departments: {Department.objects.count()}")
print(f"  Doctors: {Doctor.objects.count()}")
print(f"  Patients: {Patient.objects.count()}")
print(f"  Appointments: {Appointment.objects.count()}")
print(f"  Users: {User.objects.count()}")
print("\n🔑 Login: admin / Admin@2025")
print("="*50)