from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage),
    path("home",views.homepage),
    path("about",views.aboutpage),
    path("contact",views.contactpage),
    path("form",views.myform),
    path("myformprocess",views.myformprocess),
    path("add-student",views.addStudent),
    path("display-student",views.displayStudent),
    path("delete-student/<int:id>",views.deleteStudent,name='delete-student'),
    path("edit-student/<int:id>",views.editStudent),
]

# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ... existing paths ...
    path('add-question/', views.add_question, name='add-question'),
    path('success/', views.success_page, name='success_page'),
]
# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ... existing paths ...
    path('add-question/', views.add_question, name='add-question'),
    path('success/', views.success_page, name='success_page'),
]


from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('home/', views.homepage, name='home-page'),
    path('about/', views.aboutpage, name='about'),
    path('contact/', views.contactpage, name='contact'),
    path('add-student/', views.addStudent, name='add-student'),
    path('add-question/', views.add_question, name='add-question'),
    path('success/', views.success_page, name='success_page'),
]