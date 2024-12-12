from django.shortcuts import render
from django.http import HttpResponse

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