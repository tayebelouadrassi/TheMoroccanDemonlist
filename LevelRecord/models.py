from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator
from level.models import ClassicLevel, PlatformerLevel
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class LevelRecord(models.Model):
    record_link = models.URLField(blank=True)
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.level} - {self.player}"
    
class ClassicLevelRecord(LevelRecord):
    record_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    level = models.ForeignKey(ClassicLevel, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.level.first_victor or self.record_percentage == 100:
                self.level.first_victor = self.player
                self.level.save()

        super(ClassicLevelRecord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Classic Level Record"
        verbose_name_plural = "Classic Level Records"

class PlatformerLevelRecord(LevelRecord):
    record_time = models.DurationField(default=timedelta(minutes=30))
    level = models.ForeignKey(PlatformerLevel, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.level.record_holder:
                self.level.record_holder = self.player
                self.level.save()

        super(PlatformerLevelRecord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Platformer Level Record"
        verbose_name_plural = "Platformer Level Records"

@receiver(post_save, sender=ClassicLevelRecord)
def update_player_classic_points(sender, instance, **kwargs):
    player = instance.player
    
    total_classic_points = 0

    for level_record in player.classiclevelrecord_set.all():
        level = level_record.level
        record_percentage = level_record.record_percentage

        if record_percentage == 100:
            total_classic_points += level.points
        else:
            total_classic_points += level.points * 1/3

    if player.classic_points != total_classic_points:
        player.classic_points = total_classic_points
        player.save(update_fields=['classic_points'])
        print(player.classic_points)

@receiver(post_save, sender=PlatformerLevelRecord)
def update_player_platformer_points(sender, instance, **kwargs):
    player = instance.player
    
    total_platformer_points = 0

    for level_record in player.platformerlevelrecord_set.all():
        level = level_record.level
        total_platformer_points += level.points

    if player.platformer_points != total_platformer_points:
        player.platformer_points = total_platformer_points
        player.save(update_fields=['platformer_points'])

@receiver(post_save, sender=ClassicLevelRecord)
def update_region_classic_points(sender, instance, **kwargs):
        player = instance.player
        region = player.region
        region.classic_points = region.calculate_classic_points()
        region.save()

@receiver(post_save, sender=PlatformerLevelRecord)
def update_region_platformer_points(sender, instance, **kwargs):
        player = instance.player
        region = player.region
        region.platformer_points = region.calculate_platformer_points()
        region.save()