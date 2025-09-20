from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Student
from .forms import StudentForm

from django.contrib import messages

def demopage(request):
    return HttpResponse("<h1> ITS ME JEEL SAKHARELIYA </h1>")
def aboutpage(request):
    return render(request, 'about.html')
def contactpage(request):
    return render(request, 'contact.html')
def homepage(request):
    return render(request, 'home.html')
def myform(request):
    return render(request,'form.html')
def myformprocess(request):

    a = int(request.POST['txt1'])
    b = int(request.POST['txt2'])
    c = a + b
    return render(request,"ans.html",{'mya':a,'myb':b,'sum':c}) 

def addStudent(request):
    if request.method == 'GET':
        context = {'form':StudentForm()}
        return render(request,'add.html',context)
    elif request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Added')
            return redirect(addStudent)
        else:
            messages.error(request, 'Error In Record Add')
            return render(request, 'add.html', {'form': form})
        
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
     if request.method == 'GET':
          context = {'form': StudentForm(instance=mydata), 'id':id}
          return render(request,'edit.html',context)
     elif request.method == 'POST':
          form = StudentForm(request.POST, instance=mydata)
          if form.is_valid():
               form.save()
               messages.success(request, 'updated successfully.')
               return redirect(displayStudent)
          else:
               messages.error(request, 'errors:')
               return render(request,'edit.html',{'form':form})




from django.shortcuts import render, redirect
from .questions_model import Question 

def add_question(request):
    if request.method == 'POST':
        suggestion_text = request.POST.get('suggestion')
        if suggestion_text:
            Question.objects.create(suggestion=suggestion_text)
            return redirect('success_page')
    return render(request, 'addQuestion.html')

def success_page(request):
    return render(request, 'success.html')


# myapp/views.py

def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student_success')
    else:
        form = StudentForm()
    return render(request, 'addStudent.html', {'form': form})

# myapp/views.py

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import StudyMaterial
from django.contrib import messages

from .forms import CustomUserCreationForm
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('materials')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

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

    materials = StudyMaterial.objects.filter(user=request.user)
    return render(request, 'materials.html', {'materials': materials})
from django.shortcuts import get_object_or_404

@login_required
def delete_material_view(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, user=request.user)
    if request.method == 'POST':
        material.file.delete(save=False)
        material.delete()
        messages.success(request, f'File "{material.title}" was deleted successfully.')
    return redirect('materials')

def add_student_success(request):
    return render(request, 'add_student_success.html')

        
        
