from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import Student, Question, StudyMaterial
from .forms import StudentForm, CustomUserCreationForm

def demopage(request):
    return HttpResponse("<h1> ITS ME JEEL SAKHARELIYA </h1>")

def aboutpage(request):
    return render(request, 'about.html')

def contactpage(request):
    return render(request, 'contact.html')

def homepage(request):
    return render(request, 'home.html')

# This seems like a legacy/test view, can be removed if not needed.
def myform(request):
    return render(request,'form.html')

# This seems like a legacy/test view, can be removed if not needed.
def myformprocess(request):
    a = int(request.POST['txt1'])
    b = int(request.POST['txt2'])
    c = a + b
    return render(request,"ans.html",{'mya':a,'myb':b,'sum':c}) 

# This view handles the "Give Me Your Info" form.
# Note: The templates add.html and addStudent.html are identical.
# This view now correctly handles both GET and POST for a single form.
def addStudent(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student_success')
        else:
            # If form is invalid, re-render the page with errors.
            return render(request, 'addStudent.html', {'form': form})
    else: # GET request
        form = StudentForm()
    return render(request, 'addStudent.html', {'form': form})

def add_student_success(request):
    return render(request, 'add_student_success.html')

# These views seem to be for a separate admin-like interface.
# They can be kept if you have a custom display/edit/delete page.
def displayStudent(request):
    dbdata = Student.objects.all()
    context = {'mydata':dbdata}
    return render(request,'display.html',context)

def deleteStudent(request,id):
    mydata = get_object_or_404(Student, pk=id)
    mydata.delete()
    messages.success(request, 'Record Delete')
    return redirect(displayStudent)

def editStudent(request,id):
    mydata = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request, 'updated successfully.')
            return redirect(displayStudent)
        else:
            messages.error(request, 'errors:')
            return render(request,'edit.html',{'form':form})
    else: # GET request
        context = {'form': StudentForm(instance=mydata), 'id':id}
        return render(request,'edit.html',context)

def add_question(request):
    if request.method == 'POST':
        # The name in home.html is 'suggestion_text'
        suggestion_text = request.POST.get('suggestion_text')
        if suggestion_text:
            Question.objects.create(suggestion=suggestion_text)
            return redirect('success_page')
    # Redirect to home if accessed via GET
    return redirect('home')

def success_page(request):
    return render(request, 'success.html')

# --- Study Material Views ---

# Data for the new Study Material page. You can update the '#' with your Google Drive links.
STUDY_MATERIALS_DATA = {
    "ce0316": {
        "name": "Object Oriented Concepts with UML (OOCp)",
        "icon": "fas fa-project-diagram",
        "units": {
            "unit1": {"parts": ["UNIT-I: Introduction to C++"], "url": "https://drive.google.com/drive/folders/18eMti3I6_SuVvS5qakQrcirgbcRo_7W8"},
            "unit2": {"parts": ["UNIT-II: Objects and classes"], "url": "https://drive.google.com/drive/folders/18qnXMYmFtqAQxxQk5Z0VFQnNQqgzQTPZ"},
            "unit3": {"parts": ["UNIT-III: Inheritance"], "url": "https://drive.google.com/drive/folders/18syyX6kgnl6PMbDa42UVVdkNkyEoE-ad"},
            "unit4": {"parts": ["UNIT-IV: File management, Object Oriented Design"], "url": "https://drive.google.com/drive/folders/1ZHs0o4nuXiXxIALRjpxT3-qZeYzkUNWi"},
        }
    },
    "ce0317": {
        "name": "Database Management System (DBMS)",
        "icon": "fas fa-database",
        "units": {
            "unit1": {"parts": ["UNIT-I: Introductory concepts of DBMS"], "url": "https://drive.google.com/drive/folders/1CMjQRBqsW6AhAW2c4DqdE374rj6rTvj2"},
            "unit2": {"parts": ["UNIT-II: Entity-Relationship model, Relational Model", "Relation Database Design"], "url": "https://drive.google.com/drive/folders/1CZhqKylDv_RAwdTQufHIDaKR-nstblnV"},
            "unit3": {"parts": ["UNIT-III: Transaction Management and Security"], "url": "https://drive.google.com/drive/folders/1ZtS4WOOBR8tpoWLnNUZVZtd9xfY6ASVS"},
            "unit4": {"parts": ["UNIT-IV: SQL & PL/SQL Concepts"], "url": "https://drive.google.com/drive/folders/1KYVzH3OE448iAXubHlG5fZFQrzTZAY3G"},
        }
    },
    "ec0315": {
        "name": "Digital Electronics",
        "icon": "fas fa-microchip",
        "units": {
            "unit1": {"parts": ["UNIT-I: Number Systems"], "url": "https://drive.google.com/drive/folders/1B9n-lV5NQxy_hn4ucSyFec-AsXFCNtPv"},
            "unit2": {"parts": ["UNIT-II: Binary Codes, Logic Gates", "Boolean Algebra"], "url": "https://drive.google.com/drive/folders/1BQ14csl_RydakxossjmfcEzqD9RS5Wpn"},
            "unit3": {"parts": ["UNIT-III: Combinational circuits with MSI & LSI, Flip flop"], "url": "https://drive.google.com/drive/folders/1LH3WK6MVlC6qh3H9aBrMmmAG4UB9mt7_"},
            "unit4": {"parts": ["UNIT-IV: Shift Registers, Counters", "FSM Design"], "url": "https://drive.google.com/drive/folders/181URc0NrKaLrRSloYAUEBO04CBXLjfvU"},
        }
    },
    "math": {
        "name": "B. Tech. (Mathematics)",
        "icon": "fas fa-calculator",
        "units": {
            "unit1": {"parts": ["UNIT-I: Basics of Probability, Probability distributions"], "url": "https://drive.google.com/drive/folders/19-vJ9Jh3hddT4kc47j3lYAezHEsTaBVy"},
            "unit2": {"parts": ["UNIT-II: Statistics"], "url": "https://drive.google.com/drive/folders/19BA3xWRoozmdGdOC3gXowNLAQjjAycCE"},
            "unit3": {"parts": ["UNIT-III: Introduction, Interpolation"], "url": "https://drive.google.com/drive/folders/19Gf6BAOeTuPnsW2iQBKjiNF6on3006ZF"},
            "unit4": {"parts": ["UNIT-IV: Numerical Methods"], "url": "https://drive.google.com/drive/folders/19XL5YZS9mb0K4u6MnXcPkpW7tuoAGFAY"},
        }
    }
}

def study_material_page(request):
    return render(request, 'study_material.html', {'subjects': STUDY_MATERIALS_DATA})

def view_material(request, subject_code, unit_code):
    try:
        # Look up the URL from the data dictionary
        url = STUDY_MATERIALS_DATA[subject_code]['units'][unit_code]['url']
        
        # Check if the URL is still a placeholder
        if url == "#":
            messages.info(request, "This material is not yet available. Please check back later.")
            return redirect('public_materials')
        
        # Redirect the user to the Google Drive link
        return redirect(url)
    except KeyError:
        # If the subject or unit code is invalid, raise a 404 error
        raise Http404("The requested study material could not be found.")

def public_materials_view(request):
    query = request.GET.get('q', '')
    
    subjects_data = STUDY_MATERIALS_DATA
    
    if query:
        subjects_data = {
            code: subject for code, subject in STUDY_MATERIALS_DATA.items()
            if query.lower() in subject['name'].lower()
        }
        
    context = {'subjects': subjects_data}
    return render(request, 'study_material.html', context)

# --- Authentication Views ---
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Successfully Signed Up! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- User Materials Views ---
@login_required
def materials_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if title and file:
            StudyMaterial.objects.create(user=request.user, title=title, file=file)
            messages.success(request, 'File uploaded successfully!')
            return redirect('materials')
        else:
            messages.error(request, 'Please provide both title and file.')

    # Handle GET request for searching/listing
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest') # Default to 'newest'

    materials_list = StudyMaterial.objects.filter(user=request.user)

    # Searching logic
    if query:
        materials_list = materials_list.filter(title__icontains=query)

    # Sorting logic
    if sort_by == 'oldest':
        materials_list = materials_list.order_by('uploaded_at')
    elif sort_by == 'name_asc':
        materials_list = materials_list.order_by('title')
    elif sort_by == 'name_desc':
        materials_list = materials_list.order_by('-title')
    else: # Default to 'newest'
        materials_list = materials_list.order_by('-uploaded_at')

    # Pagination logic: Show 5 materials per page
    paginator = Paginator(materials_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    return render(request, 'materials.html', context)

@login_required
def delete_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
    if request.method == 'POST':
        material.file.delete(save=False)
        material.delete()
        messages.success(request, f'File "{material.title}" was deleted successfully.')
    return redirect('materials')

@login_required
def edit_material_title(request, material_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
        new_title = request.POST.get('title', '').strip()

        if not new_title:
            return JsonResponse({'status': 'error', 'message': 'Title cannot be empty.'}, status=400)
        
        material.title = new_title
        material.save()
        
        return JsonResponse({'status': 'success', 'message': 'Title updated successfully.', 'newTitle': new_title})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

# --- Profile AJAX Views ---
@login_required
def change_name(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not first_name or not last_name:
            return JsonResponse({'status': 'error', 'message': 'First and last name are required.'}, status=400)

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        new_name = user.first_name or user.username
        return JsonResponse({'status': 'success', 'message': 'Name updated successfully!', 'newName': new_name})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def change_password(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return JsonResponse({'status': 'success', 'message': 'Password changed successfully.'})
        else:
            errors = '. '.join([' '.join(v) for k, v in form.errors.items()])
            return JsonResponse({'status': 'error', 'message': errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
