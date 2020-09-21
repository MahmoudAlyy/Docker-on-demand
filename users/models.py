from django.db import models
from django.contrib.auth.models import User

class Machines(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="machine")
	instance_id = models.TextField()
	instance_name = models.TextField()


	def __str__(self):
		return f"{self.instance_name}"


