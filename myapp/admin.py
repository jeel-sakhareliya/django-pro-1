from django.contrib import admin

from django.contrib import admin
from .questions_model import Question

# Register your models here.
from . models import Student

admin.site.register(Student)
