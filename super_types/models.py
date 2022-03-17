from django.db import models

class SuperType(models.Model):
    name = models.CharField(max_length=255)
