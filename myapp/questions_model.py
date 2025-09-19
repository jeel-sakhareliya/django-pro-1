# myapp/questions_model.py

from django.db import models

class Question(models.Model):
    """
    Model to store user suggestions.
    """
    suggestion = models.TextField(max_length=250)
    
    def __str__(self):
        return self.suggestion[:50]  # Show the first 50 chars for admin readability