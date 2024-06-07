from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    classic_points = models.FloatField(default=0)
    platformer_points = models.FloatField(default=0)

    def __str__(self):
        return self.name