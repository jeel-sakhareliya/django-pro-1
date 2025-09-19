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

def add_student(request):
    # ... your view code ...
    pass

# myapp/views.py

from django.shortcuts import render




        
        
        
