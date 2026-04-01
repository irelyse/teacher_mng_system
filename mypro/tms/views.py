import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from functools import wraps
from .models import Users, Teacher

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

    # Convert QuerySet to Pandas DataFrame
    data = list(teachers.values('tname', 'subject', 'qualification'))
    df = pd.DataFrame(data)

    # 1. Teacher Distribution (Pie Chart by Subject)
    subject_counts = df['subject'].value_counts().reset_index()
    subject_counts.columns = ['Subject', 'Count']
    fig_pie = px.pie(subject_counts, values='Count', names='Subject', title='Teacher Distribution by Subject')
    pie_html = fig_pie.to_html(full_html=False)

    # 2. Qualification Overview (Bar Chart)
    qual_counts = df['qualification'].value_counts().reset_index()
    qual_counts.columns = ['Qualification', 'Count']
    fig_bar = px.bar(qual_counts, x='Qualification', y='Count', title='Qualification Overview', color='Qualification')
    bar_html = fig_bar.to_html(full_html=False)

    return render(request, "statistics.html", {"pie_html": pie_html, "bar_html": bar_html})

# Manage teachers page
@login_required
def manage_teacher(request):
    teachers = Teacher.objects.all()
    return render(request, "manage_teacher.html", {"teachers": teachers})

# Save teacher record
@login_required
def save_teacher(request):
    if request.method == "POST":
        teacher_id = request.POST.get("id")
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)
        else:
            teacher = Teacher()

        teacher.tname = request.POST["tname"]
        teacher.subject = request.POST["subject"]
        teacher.qualification = request.POST["qualification"]
        teacher.contact = request.POST["contact"]
        teacher.leave_record = request.POST["leave_record"]
        teacher.save()

    return redirect("manage_teacher")

# Edit teacher
@login_required
def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    if request.method == 'POST':
        teacher.tname = request.POST.get('tname')
        teacher.subject = request.POST.get('subject')
        teacher.qualification = request.POST.get('qualification')
        teacher.contact = request.POST.get('contact')
        teacher.leave_record = request.POST.get('leave_record')
        teacher.save()
        return redirect('manage_teacher')
    return render(request, "edit_teacher.html", {"teacher": teacher})

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

