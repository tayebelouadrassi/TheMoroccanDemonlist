from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator
from Player.models import Player
from Level.models import ClassicLevel, PlatformerLevel

# Create your models here.

class LevelRecord(models.Model):
    record_link = models.URLField(blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.level} - {self.player}"
    
class ClassicLevelRecord(LevelRecord):
    record_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    level = models.ForeignKey(ClassicLevel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Classic Level Record"
        verbose_name_plural = "Classic Level Records"

class PlatformerLevelRecord(LevelRecord):
    record_time = models.DurationField(default=timedelta(minutes=30))
    level = models.ForeignKey(PlatformerLevel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Platformer Level Record"
        verbose_name_plural = "Platformer Level Records"