from django.db import models
default_value = 'Unknown'

class Power(models.Model):
    name = models.CharField(max_length=255)
