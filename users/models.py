from django.db import models
from django.contrib.auth.models import User

class Machines(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="machine")
# Create your models here.
