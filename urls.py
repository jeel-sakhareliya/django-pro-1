from django.urls import path
# Correct for project-level urls.py
from myapp import views

urlpatterns = [
    # Existing page URLs
    path('', views.homepage, name='home'), # Root URL for the app
    path('about/', views.aboutpage, name='about'), # /about/
    path('contact/', views.contactpage, name='contact'), # /contact/

    # New Study Material URLs
    path('study-material/', views.study_material_page, name='study_material'),
    path('study-material/view/<str:subject_code>/<str:unit_code>/', views.view_material, name='view_material'),
    path('public-materials/', views.public_materials_view, name='public_materials'),

    # Auth URLs
    path('signup/', views.signup_view, name='signup'), # /signup/
    # login and logout are now handled by django.contrib.auth.urls, but we keep this for the view logic
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
    
    # App functionality URLs
    path('add-student/', views.addStudent, name='add-student'), # /add-student/
    path('add-student/success/', views.add_student_success, name='add_student_success'), # /add-student/success/
    path('add-question/', views.add_question, name='add-question'), # /add-question/
    path('success/', views.success_page, name='success_page'), # /success/
    path('materials/', views.materials_view, name='materials'), # /materials/
    path('materials/delete/<int:material_id>/', views.delete_material_view, name='delete_material'), # /materials/delete/1/

    # Profile AJAX URLs
    path('change-name/', views.change_name, name='change_name'),
    path('change-password/', views.change_password, name='change_password'),
    path('materials/edit/<int:material_id>/', views.edit_material_title, name='edit_material_title'),
    path('materials/download-all/', views.download_all_materials, name='download_all_materials'),
]