from django.db import models

# Create your models here.
class User(models.Model):
    name_text = models.CharField(max_length=30)
