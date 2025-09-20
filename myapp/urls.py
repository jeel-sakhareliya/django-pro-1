from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("home/", views.homepage),
    path("about/", views.aboutpage, name="about"),
    path("contact/", views.contactpage, name="contact"),
    path("form/", views.myform),
    path("myformprocess/", views.myformprocess),
    path("add-student/", views.addStudent, name="add-student"),
    path('add-student/success/', views.add_student_success, name='add_student_success'),
    path("display-student/", views.displayStudent),
    path("delete-student/<int:id>", views.deleteStudent, name='delete-student'),
    path("edit-student/<int:id>", views.editStudent),
    path('add-question/', views.add_question, name='add-question'),
    path('success/', views.success_page, name='success_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('materials/', views.materials_view, name='materials'),
    path('materials/delete/<int:material_id>/', views.delete_material_view, name='delete_material'),
]