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
    return render(request, "dashboard.html")

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

