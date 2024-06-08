import math
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Level(models.Model):
    DIFFICULTIES = [
        ('Hard Demon', 'Hard Demon'),
        ('Insane Demon', 'Insane Demon'),
        ('Extreme Demon', 'Extreme Demon'),
    ]

    id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255, choices=DIFFICULTIES, blank=True)
    youtube_link = models.URLField(blank=True)
    youtube_thumbnail = models.URLField(blank=True)
    points = models.FloatField(default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class ClassicLevel(Level):
    DURATIONS = [
        ('Tiny', 'Tiny'),
        ('Short', 'Short'),
        ('Medium', 'Medium'),
        ('Long', 'Long'),
        ('XL', 'XL'),
    ]

    ranking = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=255, choices=DURATIONS, blank=True)
    min_points = models.FloatField(default=0)
    min_completion = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    first_victor = models.ForeignKey('player.Player', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            if self.ranking == 0 or self.ranking > 150:
                self.points = 0.0
                self.min_points = 0.0
            elif self.ranking <= 150:
                self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
                self.min_points = round((500 * (1 - math.log(self.ranking, 151))) * 1/3, 2)
        else:
            self.points = None
            self.min_points = None

        super(ClassicLevel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Classic Level"
        verbose_name_plural = "Classic Levels"

class PlatformerLevel(Level):
    ranking = models.PositiveIntegerField(default=0)
    record_holder = models.ForeignKey('player.Player', on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.ranking is not None:
            self.points = round(500 * (1 - math.log(self.ranking, 151)), 2)
        else:
            self.points = None

        super(PlatformerLevel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Platformer Level"
        verbose_name_plural = "Platformer Levels"

@receiver(post_save, sender=ClassicLevel)
def update_min_completion(sender, instance, **kwargs):
    if instance.ranking > 75 and instance.min_completion != 100:
        instance.min_completion = 100
        instance.save(update_fields=['min_completion'])

@receiver(post_save, sender=ClassicLevel)
def create_classic_level_record(sender, instance, created, **kwargs):
    from levelrecord.models import ClassicLevelRecord
    if created and instance.first_victor:
        player = instance.first_victor
        if instance.youtube_link:
            record_link = instance.youtube_link
            ClassicLevelRecord.objects.create(player=player, level=instance, record_percentage=100, record_link=record_link)
        else:
            ClassicLevelRecord.objects.create(player=player, level=instance, record_percentage=100)

@receiver(post_save, sender=PlatformerLevel)
def create_platformer_level_record(sender, instance, created, **kwargs):
    from levelrecord.models import PlatformerLevelRecord
    if created and instance.record_holder:
        player = instance.record_holder
        PlatformerLevelRecord.objects.create(player=player, level=instance)