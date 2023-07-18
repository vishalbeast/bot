
from django.contrib.auth.models import User
from django.db import models

class ButtonUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    button_type = models.CharField(max_length=20)
    count = models.PositiveIntegerField(default=0)