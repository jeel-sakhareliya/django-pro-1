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