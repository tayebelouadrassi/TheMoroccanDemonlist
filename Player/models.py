from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from region.models import Region
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class PlayerManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class Player(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    classic_points = models.FloatField(default=0)
    platformer_points = models.FloatField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = PlayerManager()

    def __str__(self):
        return self.username
    
@receiver(post_save, sender=Player)
def update_player_classic_points(sender, instance, created, **kwargs):
    if not created:
        player = instance
        
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

@receiver(post_save, sender=Player)
def update_player_platformer_points(sender, instance, created, **kwargs):
    if not created:
        player = instance
        
        total_platformer_points = 0

        for level_record in player.platformerlevelrecord_set.all():
            level = level_record.level
            total_platformer_points += level.points

        if player.platformer_points != total_platformer_points:
            player.platformer_points = total_platformer_points
            player.save(update_fields=['platformer_points'])

@receiver(post_save, sender=Player)
def update_region_classic_points(sender, instance, created, **kwargs):
    if not created:
        region = instance.region
        region.classic_points = region.calculate_classic_points()
        print(region.calculate_classic_points())
        if region.classic_points == None:
            region.classic_points = 0
        print(region.calculate_classic_points())
        region.save()

@receiver(post_save, sender=Player)
def update_region_platformer_points(sender, instance, created, **kwargs):
    if not created:
        region = instance.region
        region.platformer_points = region.calculate_platformer_points()
        if region.platformer_points == None:
            region.platformer_points = 0
        region.save()