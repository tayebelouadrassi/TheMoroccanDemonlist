from django.db import models

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    classic_points = models.FloatField(default=0, null=True)
    platformer_points = models.FloatField(default=0, null=True)

    def calculate_classic_points(self):
        total_classic_points = sum(player.classic_points for player in self.player_set.all())
        self.classic_points = total_classic_points
        self.save(update_fields=['classic_points'])
        return self.classic_points

    def calculate_platformer_points(self):
        total_platformer_points = sum(player.platformer_points for player in self.player_set.all())
        self.platformer_points = total_platformer_points
        self.save(update_fields=['platformer_points'])
        return self.platformer_points

    def __str__(self):
        return self.name