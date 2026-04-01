import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.db.models import Q
import csv
from functools import wraps
from .models import Users, Teacher, Subject

# Custom session-based login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('index')
        return f(request, *args, **kwargs)
    return decorated_function

# Landing page with login form
def index(request):
    return render(request, "index.html")

# Login logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Get user by username first
            user = Users.objects.get(username=username)
            # Verify the hashed password
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                return render(request, "index.html", {'error': 'Invalid credentials'})
        except Users.DoesNotExist:
            return render(request, "index.html", {'error': 'Invalid credentials'})
    else:
        return redirect('index')

# Dashboard page
@login_required
def dashboard(request):
    # Calculate Average Leave Days using Pandas
    teachers = Teacher.objects.all()
    avg_leave = 0
    if teachers.exists():
        # Extact numeric part from leave_record (e.g. "2 days" -> 2)
        leave_data = [t.leave_record for t in teachers]
        # Clean data: convert to int, ignoring non-numbers safely
        cleaned_leave = []
        for l in leave_data:
            import re
            match = re.search(r'\d+', l)
            if match:
                cleaned_leave.append(int(match.group()))
            else:
                cleaned_leave.append(0)
        
        df = pd.DataFrame(cleaned_leave, columns=['leave'])
        avg_leave = round(df['leave'].mean(), 1)
        
    return render(request, "dashboard.html", {"avg_leave": avg_leave})

# Statistics page
@login_required
def statistics(request):
    teachers = Teacher.objects.all()
    if not teachers.exists():
        return render(request, "statistics.html", {"error": "No data available."})

    # Convert QuerySet to list of dicts. Because subjects is many-to-many, we fetch related subjects
    data = []
    for t in teachers:
        subs = ", ".join([s.name for s in t.subjects.all()])
        if not subs: subs = "Unassigned"
        data.append({
            'tname': t.tname,
            'subjects': subs,
            'qualification': t.qualification
        })
    df = pd.DataFrame(data)

    # 1. Teacher Distribution (Pie Chart by Subject)
    # Explode subjects if teachers teach multiple
    all_subjects = []
    for t in teachers:
        for s in t.subjects.all():
            all_subjects.append(s.name)
    
    if all_subjects:
        subject_counts = pd.Series(all_subjects).value_counts().reset_index()
        subject_counts.columns = ['Subject', 'Count']
        fig_pie = px.pie(subject_counts, values='Count', names='Subject', title='Teacher Distribution by Subject')
        pie_html = fig_pie.to_html(full_html=False)
    else:
        pie_html = "<p>No subjects assigned yet.</p>"

    # 2. Qualification Overview (Bar Chart)
    qual_counts = df['qualification'].value_counts().reset_index()
    qual_counts.columns = ['Qualification', 'Count']
    fig_bar = px.bar(qual_counts, x='Qualification', y='Count', title='Qualification Overview', color='Qualification')
    bar_html = fig_bar.to_html(full_html=False)

    return render(request, "statistics.html", {"pie_html": pie_html, "bar_html": bar_html})

# Manage teachers page
@login_required
def manage_teacher(request):
    search_query = request.GET.get('search', '')
    if search_query:
        teachers = Teacher.objects.filter(
            Q(tname__icontains=search_query) | 
            Q(subjects__name__icontains=search_query)
        ).distinct()
    else:
        teachers = Teacher.objects.all()
    return render(request, "manage_teacher.html", {"teachers": teachers, "search_query": search_query})

# Save teacher record
@login_required
def save_teacher(request):
    if request.method == "POST":
        teacher_id = request.POST.get("id")
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
        else:
            teacher = Teacher()

        teacher.tname = request.POST.get("tname", "")
        teacher.qualification = request.POST.get("qualification", "")
        teacher.contact = request.POST.get("contact", "")
        teacher.leave_record = request.POST.get("leave_record", "")
        teacher.status = request.POST.get("status", "Active")
        
        if 'profile_picture' in request.FILES:
            teacher.profile_picture = request.FILES['profile_picture']
        if 'cv_document' in request.FILES:
            teacher.cv_document = request.FILES['cv_document']
            
        teacher.save()
        
        # Handle subjects ManyToMany
        subject_str = request.POST.get("subjects", "")
        if subject_str:
            subject_names = [s.strip() for s in subject_str.split(',') if s.strip()]
            subject_objs = []
            for name in subject_names:
                obj, created = Subject.objects.get_or_create(name=name)
                subject_objs.append(obj)
            teacher.subjects.set(subject_objs)

    return redirect("manage_teacher")

# Edit teacher
@login_required
def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    if request.method == 'POST':
        teacher.tname = request.POST.get('tname', teacher.tname)
        teacher.qualification = request.POST.get('qualification', teacher.qualification)
        teacher.contact = request.POST.get('contact', teacher.contact)
        teacher.leave_record = request.POST.get('leave_record', teacher.leave_record)
        teacher.status = request.POST.get('status', teacher.status)
        
        if 'profile_picture' in request.FILES:
            teacher.profile_picture = request.FILES['profile_picture']
        if 'cv_document' in request.FILES:
            teacher.cv_document = request.FILES['cv_document']
            
        teacher.save()
        
        subject_str = request.POST.get('subjects', '')
        if subject_str:
            subject_names = [s.strip() for s in subject_str.split(',') if s.strip()]
            subject_objs = []
            for name in subject_names:
                obj, created = Subject.objects.get_or_create(name=name)
                subject_objs.append(obj)
            teacher.subjects.set(subject_objs)
            
        return redirect('manage_teacher')
    return render(request, "edit_teacher.html", {"teacher": teacher})

# Export to CSV
@login_required
def export_teachers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teachers_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Subjects', 'Qualification', 'Contact', 'Status', 'Leave Record'])
    
    for t in Teacher.objects.all():
        subs = ", ".join([s.name for s in t.subjects.all()])
        writer.writerow([t.tname, subs, t.qualification, t.contact, t.status, t.leave_record])
        
    return response

# Bulk Import CSV
@login_required
def import_teachers_csv(request):
    if request.method == "POST" and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return redirect('manage_teacher')
            
        file_data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(file_data)
        next(reader, None) # skip header
        
        for row in reader:
            if len(row) >= 2:
                tname = row[0].strip()
                subjects_str = row[1].strip()
                qualification = row[2].strip() if len(row) > 2 else ""
                contact = row[3].strip() if len(row) > 3 else ""
                status = row[4].strip() if len(row) > 4 else "Active"
                leave_record = row[5].strip() if len(row) > 5 else ""
                
                teacher = Teacher.objects.create(
                    tname=tname,
                    qualification=qualification,
                    contact=contact,
                    status=status,
                    leave_record=leave_record
                )
                
                if subjects_str:
                    subject_names = [s.strip() for s in subjects_str.split(',') if s.strip()]
                    for name in subject_names:
                        obj, _ = Subject.objects.get_or_create(name=name)
                        teacher.subjects.add(obj)
                        
    return redirect('manage_teacher')

# Delete teacher
@login_required
def delete_teacher(request, id):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=id)
        teacher.delete()
    return redirect('manage_teacher')

# Register
def register(request):
    if request.method == 'POST':
        names = request.POST.get('names')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Users.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken."})

        # Hash the password before saving
        hashed_password = make_password(password)
        Users.objects.create(names=names, username=username, password=hashed_password)

        return redirect('index')
    
    return render(request, "register.html")

# View users
@login_required
def view_users(request):
    users = Users.objects.all()
    return render(request, 'view_users.html', {'users': users})

