from django.db import models

class Power(models.Model):
    name = models.CharField(max_length=255)
