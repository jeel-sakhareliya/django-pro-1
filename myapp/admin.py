from django.contrib import admin
from .models import Student, StudyMaterial
from .questions_model import Question

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(StudyMaterial)