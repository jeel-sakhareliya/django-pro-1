from django.db import models

from django.db import models
from .questions_model import Question

# Create your models here.
class Student(models.Model):
    sname = models.CharField("Name" ,max_length=50,blank=False)
    smobile = models.CharField("Mobile",max_length=10)
    semail = models.CharField("Email",max_length=50)
    saddress = models.CharField("Address",max_length=50)

    def __str__(self):
        return self.sname

