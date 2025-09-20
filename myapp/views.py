from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
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
